import viztools


root = viztools.VMain("Test", "Consciencia")

label = viztools.VLabel("Hello World")
label2 = viztools.VLabel("<h1>Hello World 2</h1>")

box = viztools.VHBox()
box.addChild(label)
box.addChild(label2)
root.addChild(box)

box = viztools.VVBox()
box.addChild(label.clone())
box.addChild(label2.clone())
root.addChild(box)

menu = viztools.VMenu()
menu.addEntry("One one", label.clone())
menu.addEntry("Two", label2.clone(), True)
menu2 = menu.clone()
menu2.addEntry("Fourth", menu2.clone())
menu.addEntry("Third", menu2)
root.addChild(viztools.VStyle(menu, {
    "color": "gray"
}, "h1"))

table = viztools.VTableBrowser()
table.registerKeys(["Abcd", "Efgh", "Ijkl"])
table.addRow({
    "Abcd": 85,
    "Efgh": "Hello World",
    "Ijkl": False,
})
table.addRow({
    "Abcd": "Hello World",
    "Efgh": 85,
    "Ijkl": True,
})
table.addRow({
    "Abcd": "Hello World",
    "Efgh": 85,
    "Ijkl": True,
})
root.addChild(table)

diagram = viztools.VDiagramXy("Demo #1", "X vals", "Y vals")
diagram.setType("line")
diagram.setLabels(range(1, 12))
diagram.addDataset(range(1,11),
                   [x**2 for x in range(1,11)],
                   "dataset #1",
                   "rgba(226, 15, 33, 0.2)", "red", True, False)
diagram.addDataset(range(5,12),
                   [x**1.5 for x in range(5,11)] + [20],
                   "dataset #2",
                   "rgba(26, 35, 219, 0.2)", "blue", True, False)
root.addChild(diagram)

diagram = viztools.VDiagramRel("Demo x2")
diagram.setType("pie")
diagram.setLabels(["APPLES", "DOGS", "TREES"])
diagram.setData([42,85,128],
                ["red", "green", "blue"],
                ["red", "green", "blue"])
root.addChild(diagram)

heading = viztools.VHeading(2, "Some heading")
root.addChild(heading)

paragrapg = viztools.VParagraph("Some long text shit...")
root.addChild(viztools.VStyle(paragrapg, {
    "background-color": "black",
    "color": "white"
}))

with open("demo.html", "wb") as h:
    h.write(root.render())
