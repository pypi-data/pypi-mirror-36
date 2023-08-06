Announcement: scikit-image 0.14.1
=================================

We're happy to announce the release of scikit-image v0.14.1!

scikit-image is an image processing toolbox for SciPy that includes algorithms
for segmentation, geometric transformations, color space manipulation,
analysis, filtering, morphology, feature detection, and moreself.


This is the last major release with official support for Python 2.7. Future
releases will be developed using Python 3-only syntax.

However, 0.14 is a long-term support (LTS) release and will receive bug fixes
and backported features deemed important (by community demand) until January
1st 2020 (end of maintenance for Python 2.7; see PEP 373 for details).


For more information, examples, and documentation, please visit our website:

http://scikit-image.org



Improvements
------------

- Backport PR #3162 and #3161 on branch v0.14.x (#3383)

Other Pull Requests
-------------------

- Backport: Travis should fail on failed tests (#3169)
- Backport PR #3174 on branch v0.14.x (#3179)
- Backport PR #3110 on branch v0.14.x (#3186)
- Backport PR #3176 on branch v0.14.x (#3188)
- Backport PR #3143 on branch v0.14.x (#3190)
- Backport Cython 0.23.4 fix. PR  #3171 (#3192)
- Backport #3187 Speedup rgb2gray 0 14 x (#3193)
- Backport #3127 docfix datalocality to 0.14.x (#3195)
- Backport PR #3152 on branch v0.14.x (#3196)
- Backport PR #3157 on branch v0.14.x (#3198)
- Backport PR #3097 on branch v0.14.x (#3206)
- BF: perform computation serially (with a warning) if dask is not available (#3218)
- Backport PR #3276 on branch v0.14.x (#3281)
- Backport PR #3236 on branch v0.14.x (#3282)
- Backport PR #3292 on branch v0.14.x (#3296)
- Backport PR #3295 on branch v0.14.x (#3297)
- Backport PR #3280 on branch v0.14.x (#3301)
- Backport PR #3288 on branch v0.14.x (#3302)
- Backport #3242: handle NumPy 1.15 warnings in dependencies (#3304)
- Backport of #3238 (#3310)
- Remove deprecated `dynamic_range` in `measure.compare_psnr` (backport) (#3314)
- Backport PR #3303 on branch v0.14.x (#3336)
- Backport PR #3322 on branch v0.14.x (#3338)
- Backport PR #3315 on branch v0.14.x (#3340)
- Backport PR #3243 on branch v0.14.x (#3348)
- Backport PR #3341 on branch v0.14.x (#3349)
- Merge pull request #3357 from Carreau/meeseeksdev-config (#3358)
- Update skimage/__init__.py docstring and fix import * statement. (#3265) (#3361)
- Backport PR #3359 on branch v0.14.x (#3364)
- Backport PR #3366 on branch v0.14.x (#3369)
- Backport PR #3374 on branch v0.14.x (#3375)
- Backport PR #3370 on branch v0.14.x (#3382)
- Backport PR #3052 on branch v0.14.x (Allow float->float conversion of any range) (#3390)
- Release notes for 0.14.1 (#3395)
- Mark tests known to fail on 32bit architectures with xfail, backport to the v0.14.x branch (#3401)
- Backport PR #3337 on branch v0.14.x (Build tool: Pass tests that don't raise floating point exceptions on arm with soft-fp) (#3416)
- 0.14: Add explicit Trove version classifiers (#3417)
- Update Li thresholding (Backport of #3402) (#3420)
- Backport PR #3434 on branch v0.14.x (MNT: multiprocessing should always be avaible since we depend on python >=2.7) (#3435)

6 authors added to this release [alphabetical by last name]
-----------------------------------------------------------
- François Boulogne
- Genevieve Buckley
- Emmanuelle Gouillart
- Yaroslav Halchenko
- Mark Harfouche
- Hugo
- MeeseeksMachine
- Juan Nunez-Iglesias
- Egor Panfilov
- Johannes Schönberger
- Stefan van der Walt


6 committers added to this release [alphabetical by last name]
--------------------------------------------------------------
- Emmanuelle Gouillart
- Yaroslav Halchenko
- Mark Harfouche
- Juan Nunez-Iglesias
- Egor Panfilov
- Josh Warner


6 reviewers added to this release [alphabetical by last name]
-------------------------------------------------------------
- François Boulogne
- Mark Harfouche
- Hugo
- Juan Nunez-Iglesias
- Egor Panfilov
- Stefan van der Walt

