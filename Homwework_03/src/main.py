from triest import TriestBase

def main():
    triest_base = TriestBase(file='../data/facebook_combined.txt', M=30000, verbose=True)
    estimated_triangles = triest_base.run()
    print("Final estimated number of triangles:", estimated_triangles)

if __name__ == "__main__":
    main()