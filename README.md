# Generate atom PNGS:
mkdir outputs
python gen_atom_pngs.py

# Generate DOC file:
mkdir output_doc
python gen_doc.py

# Convert PNGs to PDF
mkdir outputs_pdf
mkdir outputs_pdf/outputs
for i in `ls outputs/*.png | sed -e 's/\.png$//'`; do convert $i.png outputs_pdf/$i.pdf ; done
mv outputs_pdf/outputs/ outputs_pdf/
rm -rf outputs_pdf/outputs

# Make GIF of images
convert $(ls outputs/*.png | sort -V) atom.gif
