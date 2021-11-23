ag.gui.NewFile();
ag.m.ClearAllErrors();
ag.m.NewSession (true);
ag.gui.setUnits(ag.c.UnitMillimeter, ag.c.UnitDegree, ag.c.No);

//Plane
// var plxy = agb.GetXYPlane();
// var pl4 = agb.PlaneFromPlane(plxy);

//Set All Parameterized Variables

var D_1 = 0.65
var D_subFrac = 0.5
var L_Total = 4.0
var L_subFrac = 0.385
var D2 = 0.385
var angle = 45.0
var compFactor = 1.0

var L1 = (L_Total*(1-L_subFrac))/2
var L2 = L_Total*L_subFrac
var D1 = D_1
var D2 = D_1*D_subFrac
var angle_deg = 90-angle
var angle_rad = (angle_deg)*Math.PI/180
var length_num = 1
var width_num = 1
var oblong = compFactor
var spacerOverlap = 0.1*D1*oblong

p2 = agb.PlaneFromPlane(agb.GetXYPlane());
if(p2)
{
    p2.Name = "Plane 2";
    p2.AddTransform(agc.XformZOffset, L1);
}

p3 = agb.PlaneFromPlane(agb.GetXYPlane());
if(p3)
{
    p3.Name = "Plane 3";
    p3.AddTransform(agc.XformZOffset, L1+L2);
}

p4 = agb.PlaneFromPlane(agb.GetXYPlane());
if(p4)
{
    p4.Name = "Plane 4";
    p4.AddTransform(agc.XformZOffset, 2*L1+L2);
}

pMirror1 = agb.PlaneFromPlane(agb.GetXYPlane());
if(pMirror1)
{
    pMirror1.Name = "Mirrow Plane";
    pMirror1.AddTransform(agc.XformZOffset, Math.cos(angle_rad));
}

function sketchCircle1 (p, r, oblong)
{
    //Plane
    p.Plane  = agb.GetXYPlane();

    //Sketch
    p.Sk1 = p.Plane.NewSketch();
    p.Sk1.Name = "Ellipse 1";
    with (p.Sk1)
    {
        p.Cr1 = Ellipse(0.00000000, 0.00000000,
            r, 0.00000,
            0.00000000, r*oblong);
    }
    return p;
}

function sketchCircle2 (p, r1, r2)
{
    //Plane
    p.Plane  = agb.GetActivePlane();
    p.Origin = p.Plane.GetOrigin();
    p.XAxis  = p.Plane.GetXAxis();
    p.YAxis  = p.Plane.GetYAxis();

    //Sketch
    p.Sk2 = p.Plane.NewSketch();
    p.Sk2.Name = "Ellipse 2";
    with (p.Sk2)
    {
        p.Cr1 = Ellipse(0.00000000, 0.00000000,
            r2*oblong, 0.00000,
            0.00000000, r2*oblong);
    }
    return p;
}

function sketchCircle3 (p, r1, r2)
{
    //Plane
    p.Plane  = agb.GetActivePlane();

    //Sketch
    p.Sk3 = p.Plane.NewSketch();
    p.Sk3.Name = "Ellipse 3";
    with (p.Sk3)
    {
        p.Cr1 = Ellipse(0.00000000, 0.00000000,
            r2*oblong, 0.0000,
            0.00000000, r2*oblong);
    }
    return p;
}

function sketchCircle4 (p, r)
{
    //Plane
    p.Plane  = agb.GetActivePlane();

    //Sketch
    p.Sk4 = p.Plane.NewSketch();
    p.Sk4.Name = "Ellipse 4";
    with (p.Sk4)
    {
        p.Cr1 = Ellipse(0.00000000, 0.00000000,
            r, 0.0000,
            0.00000000, r*oblong);
    }
    return p;
}

var ps1 = sketchCircle1 (new Object(), D1/2, oblong);
agb.SetActivePlane(p2);
var ps2 = sketchCircle2 (new Object(), D1/2, D2/2, oblong);
agb.SetActivePlane(p3);
var ps3 = sketchCircle3 (new Object(), D1/2, D2/2, oblong);
agb.SetActivePlane(p4);
var ps4 = sketchCircle4 (new Object(), D1/2, oblong);
//Finish

var Skin1 = agb.Skin(agc.Add, agc.No, 0.0, 0.0);
Skin1.Name = "Skin1"
Skin1.AddBaseObject(ps1.Sk1);
Skin1.AddBaseObject(ps2.Sk2);
// Skin1.AddBaseObject(ps3.Sk3);
// Skin1.AddBaseObject(ps4.Sk4);

agb.Regen(); //To insure model validity

var Skin1 = agb.Skin(agc.Add, agc.No, 0.0, 0.0);
Skin1.Name = "Skin2"
// Skin1.AddBaseObject(ps1.Sk1);
Skin1.AddBaseObject(ps2.Sk2);
Skin1.AddBaseObject(ps3.Sk3);
// Skin1.AddBaseObject(ps4.Sk4);

agb.Regen(); //To insure model validity

var Skin1 = agb.Skin(agc.Add, agc.No, 0.0, 0.0);
Skin1.Name = "Skin3"
// Skin1.AddBaseObject(ps1.Sk1);
// Skin1.AddBaseObject(ps2.Sk2);
Skin1.AddBaseObject(ps3.Sk3);
Skin1.AddBaseObject(ps4.Sk4);

agb.Regen(); //To insure model validity

var T1 = ag.gui.CreateBodyOp(10); // BodyopTranslate

ag.listview.ActivateItem("Preserve Bodies?");
ag.listview.ItemValue = "Yes";

ag.listview.ActivateItem("Bodies");
agb.ClearSelections();
ag.bodyPick;
ag.gui.SelectAll(); 
ag.listview.ItemValue = "Apply";

ag.listview.ActivateItem("Direction Definition");
ag.listview.ItemValue = "Coordinates";

ag.listview.ActivateItem("FD3, X Offset");
ag.listview.ItemValue = 0;

ag.listview.ActivateItem("FD4, Y Offset");
ag.listview.ItemValue = D1*oblong;

ag.listview.ActivateItem("FD5, Z Offset");
ag.listview.ItemValue = 0;

agb.Regen();

var R1 = ag.gui.CreateBodyOp(11); // BodyopTranslate
ag.listview.ActivateItem("Bodies");
agb.ClearSelections();
agb.AddSelect(agc.TypeBody, ag.fm.Body(1));
ag.listview.ItemValue = "Apply";

ag.listview.ActivateItem("Axis Definition");
ag.listview.ItemValue = "Components";
ag.listview.ActivateItem("FD7, Y Component");
ag.listview.ItemValue = 1;
ag.listview.ActivateItem("FD8, Z Component");
ag.listview.ItemValue = 0;
ag.listview.ActivateItem("FD9, Angle");
ag.listview.ItemValue = angle_deg;

var R2 = ag.gui.CreateBodyOp(11); // BodyopTranslate
ag.listview.ActivateItem("Bodies");
agb.ClearSelections();
agb.AddSelect(agc.TypeBody, ag.fm.Body(0));
ag.listview.ItemValue = "Apply";

ag.listview.ActivateItem("Axis Definition");
ag.listview.ItemValue = "Components";
ag.listview.ActivateItem("FD7, Y Component");
ag.listview.ItemValue = 1;
ag.listview.ActivateItem("FD8, Z Component");
ag.listview.ItemValue = 0;
ag.listview.ActivateItem("FD9, Angle");
ag.listview.ItemValue = -1*angle_deg;

var T2 = ag.gui.CreateBodyOp(10); // BodyopTranslate

ag.listview.ActivateItem("Preserve Bodies?");
ag.listview.ItemValue = "No";

ag.listview.ActivateItem("Bodies");
agb.ClearSelections();
agb.AddSelect(agc.TypeBody, ag.fm.Body(1));
ag.listview.ItemValue = "Apply";

ag.listview.ActivateItem("Direction Definition");
ag.listview.ItemValue = "Coordinates";

ag.listview.ActivateItem("FD3, X Offset");
ag.listview.ItemValue = 0;

ag.listview.ActivateItem("FD4, Y Offset");
ag.listview.ItemValue = -1*spacerOverlap;

ag.listview.ActivateItem("FD5, Z Offset");
ag.listview.ItemValue = 0;

var R3 = ag.gui.CreateBodyOp(11); // BodyopTranslate
ag.listview.ActivateItem("Preserve Bodies?");
ag.listview.ItemValue = "Yes";

ag.listview.ActivateItem("Bodies");
agb.ClearSelections();
agb.AddSelect(agc.TypeBody, ag.fm.Body(0));
ag.listview.ItemValue = "Apply";

ag.listview.ActivateItem("Axis Definition");
ag.listview.ItemValue = "Components";
ag.listview.ActivateItem("FD7, Y Component");
ag.listview.ItemValue = 1;
ag.listview.ActivateItem("FD8, Z Component");
ag.listview.ItemValue = 0;

ag.listview.ActivateItem("FD12, Z Coordinate");
ag.listview.ItemValue = (2*L1+L2)*Math.cos(angle_rad);

ag.listview.ActivateItem("FD9, Angle");
ag.listview.ItemValue = 180;

agb.Regen();


boxLength = 30;
boxWidth = 20;


function translateBodyLong(i, L1, L2, angle_rad) {
    ag.gui.CreateBodyOp(10);
    ag.listview.ActivateItem("Preserve Bodies?");
    ag.listview.ItemValue = "Yes";

    ag.listview.ActivateItem("Bodies");
    agb.ClearSelections();
    ag.bodyPick;
    ag.gui.SelectAll(); 
    ag.listview.ItemValue = "Apply";

    ag.listview.ActivateItem("Direction Definition");
    ag.listview.ItemValue = "Coordinates";

    ag.listview.ActivateItem("FD3, X Offset");
    ag.listview.ItemValue = (Math.pow(2,i))*(2*L1+L2)*Math.sin(angle_rad);

    ag.listview.ActivateItem("FD4, Y Offset");
    ag.listview.ItemValue = 0;

    ag.listview.ActivateItem("FD5, Z Offset");
    ag.listview.ItemValue = 0;

    agb.Regen();
}

function translateBodyWide(i, L1, L2, angle_rad) {
    ag.gui.CreateBodyOp(10);
    ag.listview.ActivateItem("Preserve Bodies?");
    ag.listview.ItemValue = "Yes";

    ag.listview.ActivateItem("Bodies");
    agb.ClearSelections();
    ag.bodyPick;
    ag.gui.SelectAll(); 
    ag.listview.ItemValue = "Apply";

    ag.listview.ActivateItem("Direction Definition");
    ag.listview.ItemValue = "Coordinates";

    ag.listview.ActivateItem("FD3, X Offset");
    ag.listview.ItemValue = 0;

    ag.listview.ActivateItem("FD4, Y Offset");
    ag.listview.ItemValue = 0;

    ag.listview.ActivateItem("FD5, Z Offset");
    ag.listview.ItemValue = (Math.pow(2,i))*(2*L1+L2)*Math.cos(angle_rad);

    agb.Regen();
}

function createPattern(L,W) {
    for(var i = 1; i< L; i++) {
        translateBodyLong(i, L1, L2, angle_rad)
    }
    for(var i = 1; i< W; i++) {
        translateBodyWide(i, L1, L2, angle_rad)
    }
}


patternL = length_num
patternW = width_num
createPattern(patternL,patternW);


function createBoundingBox(L,W, L1, L2, D1, angle_rad) {
    bodyOverlap2 = 0.3
    boxLength = (Math.pow(2,L))*(2*L1+L2)*Math.sin(angle_rad) - 2*bodyOverlap2;
    boxWidth = (Math.pow(2,W))*(2*L1+L2)*Math.cos(angle_rad) - 2*bodyOverlap2;

    // boxLength = (Math.pow(2,L))*9*Math.cos(Math.PI/4);
    // boxWidth = (Math.pow(2,W))*9*Math.cos(Math.PI/4);

    function planeSketchesOnly (p)
    {

    //Plane
        p.Plane  = agb.GetZXPlane();
        p.Origin = p.Plane.GetOrigin();
        p.XAxis  = p.Plane.GetXAxis();
        p.YAxis  = p.Plane.GetYAxis();

        //Sketch
        p.Sk1 = p.Plane.NewSketch();
        p.Sk1.Name = "Box Base";

        bodyOverlap = 0.01
        //Edges
        with (p.Sk1)
        {
            p.Ln7 = Line(0.00000000, 0.00000000, boxWidth, 0.00000000);
            p.Ln7.Name = "mainEdge1"
            p.Ln8 = Line(boxWidth, 0.00000000, boxWidth, boxLength);
            p.Ln7.Name = "mainEdge2"
            p.Ln9 = Line(boxWidth, boxLength, 0.00000000, boxLength);
            p.Ln7.Name = "mainEdge3"
            p.Ln10 = Line(0.00000000, boxLength, 0.00000000, 0.00000000);
            p.Ln7.Name = "mainEdge4"
        }
        return p;
    } //End Plane JScript function: planeSketchesOnly

    //Call Plane JScript function
    var boxBase = planeSketchesOnly (new Object());
    var ext1 = agb.Extrude(agc.Frozen, boxBase.Sk1, agc.DirNormal, agc.ExtentFixed, 2*D1*oblong-spacerOverlap-2*bodyOverlap,
    agc.ExtentFixed, 0.0, agc.No, 0.0, 0.0);

    agb.Regen();

    ag.gui.CreateBodyOp(10);
    ag.listview.ActivateItem("Preserve Bodies?");
    ag.listview.ItemValue = "NO";

    ag.listview.ActivateItem("Bodies");
    agb.ClearSelections();
    agb.AddSelect(agc.TypeBody, ag.fm.Body(1)); 
    ag.listview.ItemValue = "Apply";

    ag.listview.ActivateItem("Direction Definition");
    ag.listview.ItemValue = "Coordinates";

    ag.listview.ActivateItem("FD3, X Offset");
    ag.listview.ItemValue = -(2*L1+L2)*Math.sin(angle_rad)+bodyOverlap2;

    ag.listview.ActivateItem("FD4, Y Offset");
    ag.listview.ItemValue = -0.5*(D1*oblong)+bodyOverlap;

    ag.listview.ActivateItem("FD5, Z Offset");
    ag.listview.ItemValue = bodyOverlap2;

    agb.Regen();
}

createBoundingBox(patternL, patternW, L1, L2, D1, angle_rad)

ag.gui.CreateBoolean()
ag.listview.ActivateItem("Operation");
ag.listview.ItemValue = "Subtract";

ag.listview.ActivateItem("Tool Bodies");
agb.ClearSelections();
agb.AddSelect(agc.TypeBody, ag.fm.Body(0));
ag.listview.ItemValue = "Apply";

ag.listview.ActivateItem("Target Bodies");
agb.ClearSelections();
agb.AddSelect(agc.TypeBody, ag.fm.Body(1));
ag.listview.ItemValue = "Apply";

agb.Regen();

ag.gui.CreateBodyOp(10);
ag.listview.ActivateItem("Preserve Bodies?");
ag.listview.ItemValue = "NO";

ag.listview.ActivateItem("Bodies");
agb.ClearSelections();
agb.AddSelect(agc.TypeBody, ag.fm.Body(1)); 
ag.listview.ItemValue = "Apply";

ag.listview.ActivateItem("Direction Definition");
ag.listview.ItemValue = "Coordinates";

ag.listview.ActivateItem("FD4, Y Offset");
ag.listview.ItemValue = 0.5*(D1*oblong)-bodyOverlap;

agb.Regen();

ag.gui.CreateBodyOp(10);
ag.listview.ActivateItem("Preserve Bodies?");
ag.listview.ItemValue = "NO";

ag.listview.ActivateItem("Bodies");
agb.ClearSelections();
agb.AddSelect(agc.TypeBody, ag.fm.Body(1)); 
ag.listview.ItemValue = "Apply";

ag.listview.ActivateItem("Direction Definition");
ag.listview.ItemValue = "Coordinates";

ag.listview.ActivateItem("FD5, Z Offset");
ag.listview.ItemValue = -1*bodyOverlap2;

agb.Regen();