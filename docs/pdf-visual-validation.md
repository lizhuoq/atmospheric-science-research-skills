# PDF visual validation workflow

PDF text extraction alone is insufficient for equations, tables, multi-panel figures, axes, legends, and spatial fields. Build-time validation therefore uses a paired representation:

1. render selected pages to PNG;
2. extract page text and table candidates;
3. detect figure, table, and equation signals;
4. compare extracted structure against the rendered page;
5. store only a diagnostic manifest or source locator in public outputs;
6. remove page images and extracted text before publication.

Run locally with the bundled build environment or install `pypdfium2`, `Pillow`, and `pdfplumber`:

```powershell
python scripts/inspect_pdf_visuals.py data/papers/01/example.pdf tmp/pdf-inspection/example --max-pages 8
```

The command creates page PNGs and `manifest.json` under the chosen temporary directory. A human must inspect the rendered pages before promoting a table value, equation, figure interpretation, or axis-derived result into an evidence record. The script never makes that promotion automatically.

Public runtime Skills do not require these dependencies or access to the PDFs. This workflow belongs only to corpus construction and expert review.

