
/apps/make/Makefile-Linux-x86-64-gcc:

````
14c14
< #C_OPT += -DKDU_NO_SSSE3      # Uncomment if no compiler support for SSSE3
---
> C_OPT += -DKDU_NO_SSSE3      # Uncomment if no compiler support for SSSE3
16c16,17
< #C_OPT += -DKDU_NO_AVX2       # Uncomment if no compiler support for AVX2/FMA
---
> C_OPT += -DKDU_NO_AVX2       # Uncomment if no compiler support for AVX2/FMA
> C_OPT += -DKDU_INCLUDE_TIFF
25c26
< SSSE3FLAGS = -mssse3          # Comment out if no compiler support for SSSE3
---
> #SSSE3FLAGS = -mssse3          # Comment out if no compiler support for SSSE3
27c28
< AVX2FLAGS = -mavx2 -mfma      # Comment out if no compiler support for AVX2/FMA
---
> #AVX2FLAGS = -mavx2 -mfma      # Comment out if no compiler support for AVX2/FMA
29c30
< LIBS = -lm -lpthread # You may comment out "-lpthreads" if coresys was
---
> LIBS = -lm -lpthread -ltiff # You may comment out "-lpthreads" if coresys was
````

/coresys/make/Makefile-Linux-x86-64-gcc:

````
15c15
< #C_OPT += -DKDU_NO_SSSE3      # Uncomment if no compiler support for SSSE3
---
> C_OPT += -DKDU_NO_SSSE3      # Uncomment if no compiler support for SSSE3
17c17
< #C_OPT += -DKDU_NO_AVX2       # Uncomment if no compiler support for AVX2/FMA
---
> C_OPT += -DKDU_NO_AVX2       # Uncomment if no compiler support for AVX2/FMA
26c26
< SSSE3FLAGS = -mssse3          # Comment out if no compiler support for SSSE3
---
> #SSSE3FLAGS = -mssse3          # Comment out if no compiler support for SSSE3
28c28
< AVX2FLAGS = -mavx2 -mfma      # Comment out if no compiler support for AVX2/FMA
---
> #AVX2FLAGS = -mavx2 -mfma      # Comment out if no compiler support for AVX2/FMA
````