# Fingerprint Duplicate Detector

A professional, student-friendly Python project for learning **visual image duplicate detection**.

> **Responsible-use note:** This project compares uploaded image files and visual appearance. It does **not** identify a person, determine whether two fingerprints belong to the same person, or perform biometric identity verification.

## What this project demonstrates

- Upload and validate up to five images
- Exact file comparison using SHA-256
- Visual comparison after normalization
- Perceptual image hashing concepts
- Similarity scoring and configurable thresholds
- Side-by-side result visualization
- Clear explanations of how a match decision was made
- Unit testing and maintainable project structure

## Learning goals

This repository is designed so that a student can start with a simple Python script and gradually understand how a production-style image comparison application is organized.

### Concepts covered

| Level | Topic | What you learn |
|---|---|---|
| 1 | File validation | Paths, extensions, file sizes |
| 2 | SHA-256 | Cryptographic hashing and exact duplicate detection |
| 3 | Image normalization | Grayscale conversion and resizing |
| 4 | Perceptual hashing | Comparing image structure instead of file bytes |
| 5 | Similarity scoring | Thresholds, false positives, false negatives |
| 6 | Visualization | Explaining results with side-by-side images |
| 7 | Testing | Unit tests and regression protection |
| 8 | CI | Automated checks with GitHub Actions |
| 9 | Packaging | Clean modules and reusable services |
| 10 | Deployment roadmap | API, Docker, cloud deployment |

## How matching works

The project intentionally separates several ideas:

### 1. Exact file match

The original bytes of each image are hashed with SHA-256. If two hashes are identical, the files are byte-for-byte identical.

```text
image A -> SHA-256 -> abc123...
image B -> SHA-256 -> abc123...
             same hash
                |
                +--> exact duplicate file
```

### 2. Visual comparison

Two images can look the same while having different dimensions, formats, or compression. For that reason, the visual comparison pipeline normalizes the images before comparing them.

```text
original image
      |
      v
grayscale conversion
      |
      v
resize to common size
      |
      v
normalize intensity
      |
      v
calculate similarity
```

### 3. Threshold decision

A similarity score is compared with a configurable threshold. The threshold is a project parameter, not a claim of biometric accuracy.

## Project structure

```text
fingerprint-duplicate-detector/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── config.py
│   ├── models.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── image_loader.py
│   │   ├── exact_match.py
│   │   ├── visual_match.py
│   │   └── report.py
│   └── ui/
│       ├── __init__.py
│       └── components.py
├── tests/
├── examples/
├── docs/
│   ├── algorithms.md
│   ├── learning-guide.md
│   └── roadmap.md
├── requirements.txt
├── README.md
├── LICENSE
└── .gitignore
```

## Planned application flow

1. Upload exactly five images.
2. Validate file type and file size.
3. Display upload count.
4. Run exact-file comparison.
5. Run visual comparison for each pair.
6. Display pairwise similarity scores.
7. Trigger a clear message when a configured duplicate criterion is met.
8. Show the images and comparison explanation.

## Example result

```text
Uploaded images: 5

Upload 1 vs Upload 2
Similarity: 0.421
Result: Different visual image

Upload 1 vs Upload 5
Similarity: 0.991
Result: Visual duplicate detected
Reason: normalized image patterns are highly similar
```

The numbers above are illustrative only.

## Responsible use

Fingerprint images are sensitive biometric data in many contexts. This educational project should be run with synthetic, public-domain, or otherwise authorized sample images. Do not use it to identify people or make decisions about a person's identity.

## Roadmap

- [ ] Streamlit web interface
- [ ] Clear upload dashboard
- [ ] Difference heatmap
- [ ] Configurable similarity threshold
- [ ] Unit tests for all comparison paths
- [ ] GitHub Actions CI
- [ ] Docker support
- [ ] FastAPI service
- [ ] Performance benchmarks
- [ ] Student exercises and quizzes
- [ ] Example datasets that do not contain personal biometric information

## Local development

Python 3.11+ is recommended.

```bash
git clone https://github.com/Ranjith24490/fingerprint-duplicate-detector.git
cd fingerprint-duplicate-detector
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## License

MIT License. See `LICENSE` for details.
