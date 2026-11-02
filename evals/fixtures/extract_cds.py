"""Deliberately defective toy CDS extractor for E05; not analysis software."""

genome = "AAACCCATGTTTGGG"
start, end = 4, 9  # One-based closed feature coordinates, minus strand.
fragment = genome[start:end]
print(fragment.translate(str.maketrans("ACGT", "TGCA"))[::-1])
