# Classifier Interface Documentation

Structural diagram showing generally how all of the objects relate:

[[images/classifierInterfaceStructuralDiagram.png]]

## Major use cases.  

"Overhead" description.  

### Name a classifier glyph:
* The symbol name text field sends a message to the classifierGlyphTableView.  
* The classifierGlyphTableView goes through its array controllers and retrieves the selected Glyphs, and WriteSymbolName is called on each Glyph.  The model does the rest of the work:
* * The glyph changes its own name.
* * This field is observed by the glyph's symbolCollection, which is in turn observed by its (top level) GameraGlyphs (a classifier or a pageGlyphs object).
* * The symbol collection removes the glyph from itself.
* * The gameraGlyphs (parent) puts the glyph into the new symbol collection and removes it from the old symbol collection.
* * * The symbol collection is in charge of its own array controller.
* After all the observer pattern stuff done by the model is finished, Ratatosk sends a PATCH to /glyph/id.
* The classifierGlyphTableView tells the table views to reload.  (Note that they are both looking at the same model, so naming a classifier glyph can change the pageGlyphs table view.)

### Name a page glyph:
* Exactly the same sequence as above except it's controlled by the pageGlyphsTableView, which does the following additional thing: 
* The pageGlyphsTableView calls [classifierTableViewDelegate addGlyphs:selectedGlyphs], then the glyph is observed by both views.

## Next tasks 
Here's a summary of the status of the classifier.  Fortunately, I was able to get it to basically work - you can add page glyphs to a classifier and it all saves and arranges the views, and it uses the new /glyph/ api.  Unfortunately there are still some loose ends and some fairly necessary features, so below is a list of what I think would be the next things to deal with.

### Known issues

*  Too slow (initial load is slow and the write operation is slow.)
* Needs spinner gifs
* initial load may possibly be improved greatly by implementing and using a features=False query parameter on /classifier GET.  
* I would also investigate getting the glyphTableViews to only reload the currently visible views.  It may or may not work, I don't know, but I saw an example of that.
* CPCollectionView only lays out in a grid format with all cells the same size.  Usually, connected component output isn't very pretty, so to improve this we would need to look into rewriting CPCollectionView and making each row's height in in the collection view be individually set.  (It used to be a bigger problem, where the collection view would add a lot of space in between cells, but I dealt with that, but the cells can still be too big if one or more of the connected components too large.)
*  (loose end) there's a scroll bar bug, I believe we need to change "contentScrollView" in AppController to a regular view.  Things break if you shrink the window around the classifier interface.  This wouldn't take long.
* (loose end) issue #199 remove suggestNameForNewClassifier (also a small task.)
* After reloading Rodan, identical glyphs in the classifier view and pageglyphs view are no longer 'connected.'    
* The code would be better if the symbolCollectionArrayControllers were actually Dictionary controllers - there is a bit of linear searching of arrays going on (GameraGlyphs.j).
Needed features

* Delete glyph classifier or page glyphs 
* Guess selected glyphs (requires clever design)
* Sort pageglyphs
* Indicate selected glyph in bottom view.  
* Support larger views of the image in the bottom view (Diva?)
* Colours: classified glyphs in green, grouped glyphs in yellow, guessed glyphs in red
* After that, we're starting to get into nicer tools, like zoom, using the left table, and some toolbar tools.