# Student Learning Guide

## 1. Exact duplicate detection

SHA-256 converts file bytes into a fixed-length digest. If two digests match, the original files are byte-for-byte identical.

A resized or re-exported image can look identical while producing a different SHA-256 value.

## 2. Visual comparison

The application converts images to grayscale, resizes them to a common resolution, and normalizes brightness and contrast. It then calculates a normalized pixel-distance score.

The score is useful for learning image processing, but it is not a biometric confidence score.

## 3. Thresholds

A threshold controls how strict the visual decision is:

- Higher threshold: fewer matches, more missed visual copies.
- Lower threshold: more matches, more false positives.

Experiment with synthetic images and record the results.

## 4. Suggested exercises

1. Upload the same file twice and observe the exact-match result.
2. Resize an image and compare the exact hash with the visual score.
3. Change the threshold from 0.95 to 0.80.
4. Add brightness or compression changes and observe the score.
5. Write a unit test for an invalid image.
6. Add a new comparison algorithm and benchmark it.

## 5. Responsible use

Use only synthetic, public-domain, or authorized sample images. Do not use this educational application to identify people or make decisions about a person's identity.
