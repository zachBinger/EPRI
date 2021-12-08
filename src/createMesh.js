var basename = 'faces';
var wallNames = ['symmetry1', 'inlet', 'symmetry2', 'outlet', 'top', 'bottom'];

var DS = WB.AppletList.Applet("DSApplet").App;
// var Mesh_Mod = DS.Tree.FirstActiveBranch.MeshControlGroup;
var ListView = DS.Script.lv;

var SC = DS.Script;
var SM = SC.sm;

//select all part(bodies)
SC.doGraphicsPartSelect() //always do part selection
SC.doEditsToolbar(8047) //select all according to cursor mode


// ExtAPI.DataModel.Tree.GetObjectsByName("Solid");
var BODY_TOPO_TYPE = 3;
var FACE_TOPO_TYPE = 2;
var EDGE_TOPO_TYPE = 1;
var VERT_TOPO_TYPE = 0;

function main() {
    // First, see if we have a body selected.  If not, report to 
    // the user that a body must be selected first.
    if (SM.Parts > 0) {
        // Do the real work
        create_faces_ns_from_body();

    } else {
        SC.WBScript.Out('You must select a body before running the \
FacesFromBody.js macro.  Please select a body and re-run this \
macro.', true);
    }
}

function MyArray(){ }
MyArray.prototype = Array.prototype;
MyArray.prototype.add = Array.prototype.push;

function classify_entity_type(topo_id) {
    // The top two bits store the topological entity type within the topo
    // id value
    var type = topo_id >>> 30;
    return type;
}

function create_faces_ns_from_body() {
    // See structure definition below.
    var face_id_map = new Array(SM.Parts);
    var wall_id_map = new Array(SM.Parts);
    var spacer_id_map = new Array(SM.Parts);

    // First we want to iterate over the selected parts and create
    // a list of all of the face ids for each selected part
    for (var i = 1; i <= SM.SelectedCount; i++) {
        var topo_id = SM.SelectedEntityTopoID(i);
        var part_id = SM.SelectedPartID(i);


        // Make sure this is a body.  If not, just continue around
        if (classify_entity_type(topo_id) != BODY_TOPO_TYPE) {
            continue;
        }

        var part = SM.PartMgr.PartById(part_id);
        var brep = part.BRep;

        // Pull the body object out of the BRep structure.  The call
        // for this is the Cell function with the topological id for
        // the body of interest
        body = brep.Cell(topo_id);

        // This array will be used to hold a list of face ids for a given
        // body.
        var face_ids = new Array();
        var wall_ids = [];//new Array();
        var spacer_ids = [];//new Array();
        // These are the actual face objects associated with this body
        var faces = body.Faces;

        // Now store all of the face ids in our face id list
        for (var f = 1; f <= faces.Count; f++) {
		face_ids[face_ids.length] = faces(f).Id;
            if (faces(f).SurfaceType == 1) {
                wall_ids[wall_ids.length] = faces(f).Id;
            } else 
            {
                spacer_ids[spacer_ids.length] = faces(f).Id;
            }
        }
    face_id_map[i - 1] = new Array(2);
    face_id_map[i - 1][0] = part_id;
    face_id_map[i - 1][1] = face_ids.slice(0, face_ids.length); // Slice creates a copy of the array

    wall_id_map[i - 1] = new Array(2);
    wall_id_map[i - 1][0] = part_id;
    wall_id_map[i - 1][1] = wall_ids.slice(0, wall_ids.length); // Slice creates a copy of the array

    spacer_id_map[i - 1] = new Array(2);
    spacer_id_map[i - 1][0] = part_id;
    spacer_id_map[i - 1][1] = spacer_ids.slice(0, spacer_ids.length); // Slice creates a copy of the array
    }

    // Now that we've built up our datastructure of face ids, we need to select them all
    SM.Clear();
    var name = null;

    for (var i = 0; i < wall_id_map.length; i++) {
        var part_id = wall_id_map[i][0];
        var wall_ids = wall_id_map[i][1];
        for (var j = 0; j < wall_ids.length; j++) {
            if (j < 6) {
                SM.Clear();
                name = wallNames[j].toString();
                SM.AddToSelection(part_id, wall_ids[j], false);
                // Create the component
                SC.addNamedSelection(false, name, SC.id_NS_UnknownMultiCriterion); 
                SM.Clear();
            } else {
                SM.AddToSelection(part_id, wall_ids[j], false);
            }
                      
        }
    }

    for (var i = 0; i < spacer_id_map.length; i++) {
        var part_id = spacer_id_map[i][0];
        var spacer_ids = spacer_id_map[i][1];
        for (var j = 0; j < spacer_ids.length; j++) {
            SM.AddToSelection(part_id, spacer_ids[j], false);          
        }
    }
    name = 'spacers';
    SC.addNamedSelection(false, name, SC.id_NS_UnknownMultiCriterion);
    // Clear out the selection manager
    SM.Clear();


}

main();

SC.doGraphicsPartSelect() //always do part selection
SC.doEditsToolbar(8047) //select all according to cursor mode
SC.addNamedSelection(false, 'fluid', SC.id_NS_UnknownMultiCriterion);

var Mesh_Mod = DS.Tree.FirstActiveBranch.MeshControlGroup;
DS.Script.SelectItems(""+Mesh_Mod.ID);
var lGroupDefaults = ListView.FindGroup(2); //Get the 'Defaults' group
lGroupDefaults.Expand = 1; //Expand group
ListView.ActivateItem("Physics Preference");
ListView.ItemValue = "CFD";

ListView.ActivateItem("Element Size"); //Set 'Size' option to 'CFD'
ListView.ItemValue = 0.00005;
lGroupDefaults.Expand = 0; //Collapse group

//Set options in 'Sizing' group
var lGroupSizing = ListView.FindGroup(3);
lGroupSizing.Expand = 1; //Expand

ListView.ActivateItem("Max Size");
ListView.ItemValue = 0.00005;

DS.Script.doInsertMeshSize(1)
ListView.ActivateItem("Scoping Method");
ListView.ItemValue = "Named Selection" ;
ListView.ActivateItem("Named Selection");
ListView.ItemValue = "bottom" ;
ListView.ActivateItem("Element Size");
ListView.ItemValue = "0.000005"
ListView.ActivateItem("Growth Rate");
ListView.ItemValue = 1.2

//Set sizing options
// ListView.ActivateItem("Capture Proximity");
// ListView.ItemValue = "Yes";

//Set sizing options
// ListView.ActivateItem("Num Cells Across Gap");
// ListView.ItemValue = 10;

// //Set sizing options
// ListView.ActivateItem("Proximity Min Size");
// ListView.ItemValue = 0.0000001;

// //Set sizing options
// ListView.ActivateItem("Defeature Size");
// ListView.ItemValue = 0.0000001;

DS.Script.doInsertInflation(1)
ListView.ActivateItem("Scoping Method");
ListView.ItemValue = "Named Selection" ;
ListView.ActivateItem("Named Selection");
ListView.ItemValue = "fluid" ;
ListView.ActivateItem("Boundary Scoping Method");
ListView.ItemValue = "Named Selections" ;
ListView.ActivateItem("Boundary");
ListView.ItemValue = "bottom"
ListView.ActivateItem("Inflation Option");
ListView.ItemValue = "First Layer Thickness" ;
ListView.ActivateItem("First Layer Height");
ListView.ItemValue = "0.0000001"
ListView.ActivateItem("Maximum Layers");
ListView.ItemValue = "10"
ListView.ActivateItem("Growth Rate");
ListView.ItemValue = "1.2"

//Generate Mesh
DS.Script.doModelPreviewMeshFromToolbar(1)
DS.Script.doFileExport("/groups/achilli/EPRI2021/meshes/scriptedMeshes/batch1/mesh_X.msh")