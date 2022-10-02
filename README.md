# PreciseEdge-v-GrabCut
Comparison of PreciseEdge and GrabCut 

## Abstract

Abstract 
Computer vision is a tool that could provide livestock producers with digital body measures and records that are important for animal health and production, namely body height and length, and chest girth. However, to build these tools, the scarcity of labeled training data sets with uniform images (pose, lighting) that also represent real-world livestock can be a challenge. Collecting images in a standard way, with manual image labeling is the gold standard to create such training data, but the time and cost can be prohibitive. We introduce the PreciseEdge image segmentation algorithm to address these issues by employing a standard image collection protocol with a semi-automated image labeling method, and and a highly precise image segmentation for automated body measurement extraction directly from each image. These elements, from image collection to extraction are designed to work together to yield values highly correlated to real-world body measurements. PreciseEdge adds a brief preprocessing step inspired by chromakey to a modified GrabCut procedure to generate image masks for data extraction (body measurements) directly from the images. Three hundred RGB (red, green, blue) image samples were collected uniformly per the African Goat Improvement Network Image Collection Protocol (AGIN-ICP), which prescribes camera distance, poses, a blue backdrop, and a custom AGIN-ICP calibration sign. Images were taken in natural settings outdoors and in barns under high and low light, using a Ricoh digital camera producing JPG images (converted to PNG prior to processing). The rear and side AGIN-ICP poses were used for this study. PreciseEdge and GrabCut image segmentation methods were compared for differences in user input required to segment the images. The initial bounding box image output was captured for visual comparison. Automated digital body measurements extracted were compared to manual measures for each method. Both methods allow additional optional refinement (mouse strokes) to aid the segmentation algorithm. These optional mouse strokes were captured automatically and compared. Stroke count distributions for both methods were not normally distributed per Kolmogorov-Smirnov tests. Non-parametric Wilcoxon tests showed the distributions were different (p< 0.001) and the GrabCut stroke count was significantly higher (p=5.115 e-49), with a mean of 577.08 (std 248.45) versus 221.57 (std 149.45) with PreciseEdge. Digital body measures were highly correlated to manual height, length, and girth measures, (0.931, 0.943, 0.893) for PreciseEdge and (0.936, 0. 944, 0.869) for GrabCut (Pearson correlation coefficient). PreciseEdge image segmentation allowed for masks yielding accurate digital body measurements highly correlated to manual, real-world measurements with over 38% less user input for an efficient, reliable, non-invasive alternative to livestock hand-held direct measuring tools.
