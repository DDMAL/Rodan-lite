> https://github.com/DDMAL/Rodan/wiki/Rodan-worker

| Worker         | Notes                                                                                                      |
| -------------- | ---------------------------------------------------------------------------------------------------------- |
| python3-celery | Contains `pixel_wrapper`, `neon_wrapper`, and `gamera`                                                     |
| python2-celery | Contains all `rodan-main`'s jobs, previously known as `rodan-main`                                         |
| gpu-celery     | Contains `Text Alignment`, `Background Removal`, `SAE_binarization`, and `Paco classifier` that run on GPU |
