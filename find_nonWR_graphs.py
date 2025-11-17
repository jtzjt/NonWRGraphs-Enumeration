import subprocess
import networkx as nx
import zipfile
import argparse


# ============================================================
#  3-colorability check
# ============================================================

def is_3_colorable(G):
    order = sorted(G.nodes(), key=lambda v: -G.degree[v])
    color = {}

    def dfs(i):
        if i == len(order):
            return True
        v = order[i]
        forbidden = {color[u] for u in G.neighbors(v) if u in color}
        for c in range(3):
            if c not in forbidden:
                color[v] = c
                if dfs(i + 1):
                    return True
                del color[v]
        return False

    return dfs(0)


# ============================================================
#  Semi-transitive orientation check
# ============================================================

def has_semi_transitive_orientation(G):
    n = G.number_of_nodes()
    deg = dict(G.degree())
    edges = sorted(G.edges(), key=lambda e: -(deg[e[0]] + deg[e[1]]))
    m = len(edges)
    dir_out = {v: set() for v in G.nodes()}

    def creates_cycle(u, v):
        stack = [v]
        seen = set()
        while stack:
            x = stack.pop()
            if x == u:
                return True
            for y in dir_out[x]:
                if y not in seen:
                    seen.add(y)
                    stack.append(y)
        return False

    def has_shortcut():
        for start in G.nodes():
            stack = [(start, [start])]
            while stack:
                cur, path = stack.pop()
                for nxt in dir_out[cur]:
                    if nxt in path:
                        continue
                    np = path + [nxt]
                    L = len(np)
                    if L >= 3:
                        v0, vk = np[0], np[-1]
                        if vk in dir_out[v0]:
                            for i in range(L):
                                for j in range(i + 1, L):
                                    if np[j] not in dir_out[np[i]]:
                                        return True
                    if L < n:
                        stack.append((nxt, np))
        return False

    def dfs(i):
        if i == m:
            return not has_shortcut()
        u, v = edges[i]
        if not creates_cycle(u, v):
            dir_out[u].add(v)
            if dfs(i + 1):
                return True
            dir_out[u].remove(v)
        if not creates_cycle(v, u):
            dir_out[v].add(u)
            if dfs(i + 1):
                return True
            dir_out[v].remove(u)
        return False

    return dfs(0)


def is_word_representable(G):
    return is_3_colorable(G) or has_semi_transitive_orientation(G)


# ============================================================
#  MAIN: enumerate connected non-isomorphic graphs of order n
# ============================================================

def main(n):
    print(f"Enumerating connected non-isomorphic graphs on {n} vertices...")
    cmd = ["geng", "-c", str(n)]

    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, text=True)

    nonwr = []
    total = 0

    for line in proc.stdout:
        g6 = line.strip()
        if not g6:
            continue
        total += 1
        G = nx.from_graph6_bytes(g6.encode())
        if not is_word_representable(G):
            nonwr.append((g6, G))
            print(f"Found non-WR #{len(nonwr)}")

    proc.wait()

    print("\n==========================================")
    print(f"Total connected graphs: {total}")
    print(f"Non-word-representable: {len(nonwr)}")
    print("==========================================\n")

    zipname = f"{n}vertex_nonWR.zip"
    with zipfile.ZipFile(zipname, "w", zipfile.ZIP_DEFLATED) as z:
        for i, (g6, G) in enumerate(nonwr, start=1):
            mat = []
            for a in range(n):
                row = "".join("1" if G.has_edge(a, b) else "0" for b in range(n))
                mat.append(row)
            content = "\n".join(mat) + "\n"
            z.writestr(f"nonWR_{i}.txt", content)

    print(f"Saved ZIP → {zipname}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("n", type=int, help="number of vertices")
    args = parser.parse_args()

    main(args.n)
