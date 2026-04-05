@echo off
pandoc Book.md -o learning_to_see.epub --metadata title="Learning to See" --metadata author="Jeff Hegedus" --epub-cover-image=learning_to_see.png --toc --toc-depth=1
