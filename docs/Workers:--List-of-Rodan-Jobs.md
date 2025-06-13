Currently, Rodan jobs are divided into 3 groups: Base jobs, Python3 jobs, and GPU jobs. You can see more detailed information on required ports and authors at the source files or by opening the jobs in Rodan. To see how these jobs can be implemented in a workflow, see DDMAL's [End-to-End OMR Workflow Documentation](http://ddmal.music.mcgill.ca/e2e-omr-documentation/).

## Base jobs

- [Resource Distributor](https://github.com/DDMAL/Rodan/blob/c578706fed0cc7e062306d14db1513f569033de5/rodan-main/code/rodan/jobs/resource_distributor.py#L8): Specifies the eligible resource types for input.

- [Labeler](https://github.com/DDMAL/Rodan/blob/c578706fed0cc7e062306d14db1513f569033de5/rodan-main/code/rodan/jobs/labeler.py#L8): Add label to resources.

## Python3 jobs

### [Hello World Jobs](https://github.com/DDMAL/Rodan/blob/c578706fed0cc7e062306d14db1513f569033de5/rodan-main/code/rodan/jobs/helloworld/helloworld.py)

    These jobs' sole functions are to test basic Rodan functionalities such as job queues, input/output ports, etc.

- [Hello World](https://github.com/DDMAL/Rodan/blob/c578706fed0cc7e062306d14db1513f569033de5/rodan-main/code/rodan/jobs/helloworld/helloworld.py#L4): Output string "Hello World"
- [Hello World - Python3](https://github.com/DDMAL/Rodan/blob/c578706fed0cc7e062306d14db1513f569033de5/rodan-main/code/rodan/jobs/helloworld/helloworld.py#L114): Output string "Hello World", using a different celery queue.
- [Hello World Multiple Ports](https://github.com/DDMAL/Rodan/blob/c578706fed0cc7e062306d14db1513f569033de5/rodan-main/code/rodan/jobs/helloworld/helloworld.py#L52): Concatenate all input files and append "Hello World MultiPort"

### [Mei2Volpiano](https://github.com/DDMAL/Rodan/tree/master/rodan-main/code/rodan/jobs/mei2vol_wrapper)

    A wrapper for the library to implement it as a Rodan Job

See the [MEI2Volpiano](https://github.com/DDMAL/MEI2Volpiano) repo.

- [Mei2Volpiano](https://github.com/DDMAL/Rodan/blob/c578706fed0cc7e062306d14db1513f569033de5/rodan-main/code/rodan/jobs/mei2vol_wrapper/m2v_wrapper.py#L10): Converts MEI or XML files into volpiano strings.

### [PIL-Rodan jobs](https://github.com/DDMAL/Rodan/tree/c578706fed0cc7e062306d14db1513f569033de5/rodan-main/code/rodan/jobs/pil_rodan)

    Wrappers for PIL tasks in Rodan.

- [Red Filtering](https://github.com/DDMAL/Rodan/blob/c578706fed0cc7e062306d14db1513f569033de5/rodan-main/code/rodan/jobs/pil_rodan/red_filtering.py): Filters a spectrum of red color from image

- [Resize Image](https://github.com/DDMAL/Rodan/blob/c578706fed0cc7e062306d14db1513f569033de5/rodan-main/code/rodan/jobs/pil_rodan/resize.py): Resize an image.

- [PNG (RGB)](https://github.com/DDMAL/Rodan/blob/c578706fed0cc7e062306d14db1513f569033de5/rodan-main/code/rodan/jobs/pil_rodan/resize.py): Convert image to png format

- [TIFF](https://github.com/DDMAL/Rodan/blob/c578706fed0cc7e062306d14db1513f569033de5/rodan-main/code/rodan/jobs/pil_rodan/to_tiff.py): Convert image to tiff format

### [Gamera-4 Jobs](https://github.com/DDMAL/Rodan/tree/c578706fed0cc7e062306d14db1513f569033de5/rodan-main/code/rodan/jobs/gamera_rodan)

See more information of the Gamera 4 Package [here](https://github.com/DDMAL/Rodan/wiki/Note-on-Gamera-4-Package)

- [Non-Interactive Classifier](https://github.com/DDMAL/Rodan/blob/c578706fed0cc7e062306d14db1513f569033de5/rodan-main/code/rodan/jobs/gamera_rodan/wrappers/classification.py#L43): Performs classification on a binarized staff-less image and outputs an xml file.

- [CC Analysis](https://github.com/DDMAL/Rodan/blob/c578706fed0cc7e062306d14db1513f569033de5/rodan-main/code/rodan/jobs/gamera_rodan/wrappers/plugins/cc_analysis.py#L38C7-L38C17): Performs connected component analysis on the image.

- [Invert](https://github.com/DDMAL/Rodan/blob/c578706fed0cc7e062306d14db1513f569033de5/rodan-main/code/rodan/jobs/gamera_rodan/wrappers/plugins/image_utilities.py#L37): Invert the image

- #### [Binarization Jobs](https://github.com/DDMAL/Rodan/blob/c578706fed0cc7e062306d14db1513f569033de5/rodan-main/code/rodan/jobs/gamera_rodan/wrappers/plugins/binarization.py)

  - [Gatos Background](https://github.com/DDMAL/Rodan/blob/c578706fed0cc7e062306d14db1513f569033de5/rodan-main/code/rodan/jobs/gamera_rodan/wrappers/plugins/binarization.py#L38): Estimates the background of an image according to Gatos et al.'s method.

    Reference: _Gatos, Basilios, Ioannis Pratikakis, and Stavros_
    _J. Perantonis. 2004. An adaptive binarization technique for low_
    _quality historical documents. \*Lecture Notes in Computer_
    _Science\* 3163: 102--113._

  - [Gatos Threshold](https://github.com/DDMAL/Rodan/blob/c578706fed0cc7e062306d14db1513f569033de5/rodan-main/code/rodan/jobs/gamera_rodan/wrappers/plugins/binarization.py#L130): Thresholds an image according to Gatos et al.'s method.

    Reference: _Gatos, Basilios, Ioannis Pratikakis, and Stavros_
    _J. Perantonis. 2004. An adaptive binarization technique for low_
    _quality historical documents. \*Lecture Notes in Computer_
    _Science\* 3163: 102--113._

  - [Brink Threshold](https://github.com/DDMAL/Rodan/blob/c578706fed0cc7e062306d14db1513f569033de5/rodan-main/code/rodan/jobs/gamera_rodan/wrappers/plugins/binarization.py#L244): Calculates threshold for image with Brink and Pendock's minimum-cross  
     entropy method and returns corrected image. It is best used for binarising
    images with dark, near-black foreground and significant bleed-through.
    To that end, it generally predicts lower thresholds than other
    thresholding algorithms.

    Reference: A.D. Brink, N.E. Pendock: Minimum cross-entropy threshold selection.
    Pattern Recognition 29 (1), 1996. 179-188.

  - [Sauvola Threshold](https://github.com/DDMAL/Rodan/blob/c578706fed0cc7e062306d14db1513f569033de5/rodan-main/code/rodan/jobs/gamera_rodan/wrappers/plugins/binarization.py#L309): Creates a binary image using Sauvola's adaptive algorithm.

    Reference: Sauvola, J. and M. Pietikainen. 2000. Adaptive document image
    binarization. _Pattern Recognition_ 33: 225--236.

  - [Niblack Threshold](https://github.com/DDMAL/Rodan/blob/c578706fed0cc7e062306d14db1513f569033de5/rodan-main/code/rodan/jobs/gamera_rodan/wrappers/plugins/binarization.py#L309): Creates a binary image using Niblack's adaptive algorithm.

    Reference: Niblack, W. 1986. _An Introduction to Digital Image Processing._ Englewood
    Cliffs, NJ: Prentice Hall.

- #### [Image Conversion jobs](https://github.com/DDMAL/Rodan/blob/c578706fed0cc7e062306d14db1513f569033de5/rodan-main/code/rodan/jobs/gamera_rodan/wrappers/plugins/image_conversion.py)

  - [Convert to RGB PNG](https://github.com/DDMAL/Rodan/blob/c578706fed0cc7e062306d14db1513f569033de5/rodan-main/code/rodan/jobs/gamera_rodan/wrappers/plugins/image_conversion.py#L39)
  - [Convert to greyscale PNG](https://github.com/DDMAL/Rodan/blob/c578706fed0cc7e062306d14db1513f569033de5/rodan-main/code/rodan/jobs/gamera_rodan/wrappers/plugins/image_conversion.py#L115)
  - [Convert to greyscale 16 PNG](https://github.com/DDMAL/Rodan/blob/c578706fed0cc7e062306d14db1513f569033de5/rodan-main/code/rodan/jobs/gamera_rodan/wrappers/plugins/image_conversion.py#L192)
  - [Convert to one-bit (black and white) PNG](https://github.com/DDMAL/Rodan/blob/c578706fed0cc7e062306d14db1513f569033de5/rodan-main/code/rodan/jobs/gamera_rodan/wrappers/plugins/image_conversion.py#L268): Converts the given image to a ONEBIT image. First, the image is converted
    and then the otsu*threshold* algorithm is applied.
    For other ways to convert to ONEBIT images, see the Binarization\_ category.

- #### [Morphology](https://github.com/DDMAL/Rodan/blob/c578706fed0cc7e062306d14db1513f569033de5/rodan-main/code/rodan/jobs/gamera_rodan/wrappers/plugins/morphology.py#L7)

  - [Despeckle](https://github.com/DDMAL/Rodan/blob/c578706fed0cc7e062306d14db1513f569033de5/rodan-main/code/rodan/jobs/gamera_rodan/wrappers/plugins/morphology.py#L38): Removes connected components that are smaller than the given size.

  - [Dilate](https://github.com/DDMAL/Rodan/blob/c578706fed0cc7e062306d14db1513f569033de5/rodan-main/code/rodan/jobs/gamera_rodan/wrappers/plugins/morphology.py#L123): Morpholgically dilates the image with a 3x3 square structuring element.

- #### [Threshold](https://github.com/DDMAL/Rodan/blob/c578706fed0cc7e062306d14db1513f569033de5/rodan-main/code/rodan/jobs/gamera_rodan/wrappers/plugins/threshold.py)

  - [Otsu Threshold](https://github.com/DDMAL/Rodan/blob/c578706fed0cc7e062306d14db1513f569033de5/rodan-main/code/rodan/jobs/gamera_rodan/wrappers/plugins/threshold.py#L38): Creates a binary image by splitting along a threshold value determined using the Otsu algorithm.

    Reference: N. Otsu: A Threshold Selection Method from Grey-Level Histograms. IEEE Transactions on Systems, Man, and Cybernetics (9), pp. 62-66 (1979)

  - [Tsai Moment Preserving Threshold](https://github.com/DDMAL/Rodan/blob/c578706fed0cc7e062306d14db1513f569033de5/rodan-main/code/rodan/jobs/gamera_rodan/wrappers/plugins/threshold.py#L120): Finds a threshold point using the Tsai Moment Preserving threshold algorithm.

    Reference: W.H. Tsai: _Moment-Preserving Thresholding: A New Approach._ Computer Vision Graphics and Image Processing (29), pp. 377-393(1985)

  - [Abutaleb locally-adaptive threshold](https://github.com/DDMAL/Rodan/blob/c578706fed0cc7e062306d14db1513f569033de5/rodan-main/code/rodan/jobs/gamera_rodan/wrappers/plugins/threshold.py#L196): Creates a binary image by using the Abutaleb locally-adaptive thresholding algorithm.

  - [Bernsen threshold](https://github.com/DDMAL/Rodan/blob/c578706fed0cc7e062306d14db1513f569033de5/rodan-main/code/rodan/jobs/gamera_rodan/wrappers/plugins/threshold.py#L276): Creates a binary image by using the Bernsen algorithm.

    Reference: J. Bernsen: _Dynamic thresholding of grey-level images._
    Proc. 8th International Conference on Pattern Recognition (ICPR8),
    pp. 1251-1255, 1986.

  - [DjVu threshold](https://github.com/DDMAL/Rodan/blob/c578706fed0cc7e062306d14db1513f569033de5/rodan-main/code/rodan/jobs/gamera_rodan/wrappers/plugins/threshold.py#L403): Creates a binary image by using the DjVu thresholding algorithm.

    Reference: Bottou, L., P. Haffner, P. G. Howard, P. Simard, Y. Bengio and
    Y. LeCun. 1998. High Quality Document Image Compression with
    DjVu. AT&T Labs, Lincroft, NJ. http://research.microsoft.com/~patrice/PDF/jei.pdf

- #### [MusicStaves Toolkit](https://github.com/DDMAL/Rodan/tree/c578706fed0cc7e062306d14db1513f569033de5/rodan-main/code/rodan/jobs/gamera_rodan/wrappers/toolkits/music_staves)
      MusicStaves Toolkit is a plugin for Gamera.
  See Rodan-MusicStaves documentation [here](https://github.com/DDMAL/Rodan/wiki/Note-on-Gamera-4-Package#musicstaves-toolkit).
  - [Miyao Staff Finder](https://github.com/DDMAL/Rodan/blob/c578706fed0cc7e062306d14db1513f569033de5/rodan-main/code/rodan/jobs/gamera_rodan/wrappers/toolkits/music_staves/miyao.py#L16): use Miyao staff finding algorithm to detect staff lines.

### [Heuristic Pitch Finding](https://github.com/DDMAL/Rodan/tree/master/rodan-main/code/rodan/jobs/heuristic_pitch_finding)

    Heuristic Pitch Finding jobs utilize Gamera and the MusicStaves Toolkit but is presented as a separate category.

- [Miyao Staff Finding](https://github.com/DDMAL/Rodan/blob/c578706fed0cc7e062306d14db1513f569033de5/rodan-main/code/rodan/jobs/heuristic_pitch_finding/base.py#L18): Finds the location of staves in an image and returns them as a JSOMR file.
  This job uses the same Gamera - MusicStaves function as the Miyao Staff Finder job but with differences in input types and output formats.
- [Heuristic Pitch Finding](https://github.com/DDMAL/Rodan/blob/c578706fed0cc7e062306d14db1513f569033de5/rodan-main/code/rodan/jobs/heuristic_pitch_finding/base.py#L120): Calculates pitch values for Classified Connected Componenets from a JSOMR containing staves, and returns the results as a JSOMR file

### [MEI Encoding](https://github.com/DDMAL/Rodan/tree/master/rodan-main/code/rodan/jobs/MEI_encoding)

- [MEI Encoding](https://github.com/DDMAL/Rodan/blob/c578706fed0cc7e062306d14db1513f569033de5/rodan-main/code/rodan/jobs/MEI_encoding/MEI_encoding.py#L10): Builds an MEI file from pitchfinding information and transcript alignment results.

### [MEI Resizing](https://github.com/DDMAL/Rodan/tree/master/rodan-main/code/rodan/jobs/MEI_resizing)

- [MEI Resizing](https://github.com/DDMAL/Rodan/blob/c578706fed0cc7e062306d14db1513f569033de5/rodan-main/code/rodan/jobs/MEI_resizing/mei_resize.py#L31): Scale the facsimile of an MEI file

### [Diagonal Neume Slicing](https://github.com/DDMAL/Rodan/tree/master/rodan-main/code/rodan/jobs/diagonal_neume_slicing)

- [Diagonal Neume Slicing](https://github.com/DDMAL/Rodan/blob/c578706fed0cc7e062306d14db1513f569033de5/rodan-main/code/rodan/jobs/diagonal_neume_slicing/base.py#L16): A tool for splitting neumes into neume components based on diagonal projection.
- [Dirty Layer Repair](https://github.com/DDMAL/Rodan/blob/c578706fed0cc7e062306d14db1513f569033de5/rodan-main/code/rodan/jobs/diagonal_neume_slicing/base.py#L178): A tool for \'repairing\' broken layers by adding errors from a dirty layer. For example, using a text layer to repair its neume layer.

### [Column Splitting](https://github.com/DDMAL/Rodan/tree/develop/rodan-main/code/rodan/jobs/column_split)

- [Column Splitting](https://github.com/DDMAL/Rodan/blob/develop/rodan-main/code/rodan/jobs/column_split/base.py): Takes a multi column image and number of columns as input, returns an image with all columns vertically stacked.

### [Staff Distance Finding](https://github.com/DDMAL/Rodan/tree/develop/rodan-main/code/rodan/jobs/staff_distance)

- [Staff Distance Finding](https://github.com/DDMAL/Rodan/blob/develop/rodan-main/code/rodan/jobs/staff_distance/base.py): Outputs the approximate distance in pixels between staff lines and the ratio between the ideal distance (64px) and the approximate distance.

### <u>RODAN REMOTE JOBS</u>

    Rodan contains 2 remote jobs that exist outside of the Rodan repository code base and are installed and built separately.

- [Neon](https://github.com/DDMAL/Neon): Neume Editor Online.
  Neon is a browser-based music notation editor written in JavaScript using the Verovio music engraving library. The editor can be used to manipulate digitally encoded early musical scores in square-note notation.
- [Pixel](https://github.com/DDMAL/Pixel.js): Pixel.js is a drawing and layering plugin that works on top of Diva.js.

They are installed into Rodan through wrappers: [Neon wrapper](https://github.com/DDMAL/neon_wrapper) and [Pixel_wrapper](https://github.com/DDMAL/pixel_wrapper).

## GPU jobs

(currently not compatible with Apple Silicon chips for local deployment. See more [here](https://github.com/DDMAL/Rodan/wiki/Running-Rodan-on-ARM))

### [Text Alignment](https://github.com/DDMAL/Rodan/tree/c578706fed0cc7e062306d14db1513f569033de5/rodan-main/code/rodan/jobs/text_alignment)

- [Text Alignment](https://github.com/DDMAL/Rodan/blob/c578706fed0cc7e062306d14db1513f569033de5/rodan-main/code/rodan/jobs/text_alignment/text_alignment.py#L14): Given a text layer image and a transcript of some text on that page, finds the
  positions of each syllable of text in the transcript on the image.
  Reference: de Reuse and Fujinaga, "Robust Transcript Alignment on Medieval Chant Manuscripts," in Proceedings of the 2nd International Workshop on Reading Music Systems, 2019

### [Paco Classifier](https://github.com/DDMAL/Rodan/tree/master/rodan-main/code/rodan/jobs/Paco_classifier)

- [Training model for Patchwise Analysis of Music Document, Training](https://github.com/DDMAL/Rodan/blob/c578706fed0cc7e062306d14db1513f569033de5/rodan-main/code/rodan/jobs/Paco_classifier/fast_paco_trainer.py#L27): The job performs the training of many Selection Auto-Encoder model for the pixelwise analysis of music document images.

- [Fast Pixelwise Analysis of Music Document, Classifying](https://github.com/DDMAL/Rodan/blob/c578706fed0cc7e062306d14db1513f569033de5/rodan-main/code/rodan/jobs/Paco_classifier/fast_paco_classifier.py#L29): Given a pre-trained Convolutional neural network, the job performs a (fast) pixelwise analysis of music document images.

### [Background Removal](https://github.com/DDMAL/Rodan/tree/master/rodan-main/code/rodan/jobs/background_removal)

- [Background Removal](https://github.com/DDMAL/Rodan/blob/c578706fed0cc7e062306d14db1513f569033de5/rodan-main/code/rodan/jobs/background_removal/BgRemovalRodan.py#L6): Use Sauvola threshold to remove background.

### [SAE Binarization](https://github.com/DDMAL/Rodan/tree/master/rodan-main/code/rodan/jobs/SAE_binarization)

- [SAE Binarization](https://github.com/DDMAL/Rodan/blob/c578706fed0cc7e062306d14db1513f569033de5/rodan-main/code/rodan/jobs/SAE_binarization/SAE_binarization.py#L6): Uses Neural Network Model to perform background removal.
