# GEOLOGICAL REPORT SIMILARITY ANALYSIS USING ENTITIES

Our project aims to perform a comprehensive analysis of geological reports, extracting and comparing text content to discover patterns and insights relevant to geological exploration. The main dataset used is the WAMEX (Western Australian Mineral Exploration) dataset, containing more than 30,000 text-based reports.

The methodology follows six main steps:
1. Human Annotation: Using DataTorch for accurate ground truth in text content extraction.
2. Entity Detection: Employing PDFMiner for layout analysis to detect entities in reports.
3. Post-processing and Text Content Extraction: Aligning bounding boxes from PDFMiner with annotated counterparts from DataTorch to extract relevant text content.
4. Similarity Calculation: Using metadata JSON files and the "table_of_contents" from annotated JSON files for similarity analysis using cosine similarity and TF-IDF methods.
5. Hierarchical Clustering: Grouping similar reports using a distance metric derived from cosine similarity scores.
6. Human Checking: Verifying the effectiveness of the method by sampling and human validation.

The results are presented through a webpage developed using Gradio where users input a file name, file path, and the number of similar documents they want to generate. The output displays documents similar to the inputted file name, along with a short abstract and the pdf name for each output file.
