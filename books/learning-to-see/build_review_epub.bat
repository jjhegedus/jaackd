@echo off
pandoc title_page.md Book.md -o learning_to_see_review.epub --metadata title="Learning to See" --metadata author="Jeff Hegedus" --epub-cover-image=learning_to_see_cover.jpg --toc --toc-depth=1
