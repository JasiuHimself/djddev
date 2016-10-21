function Calendar(){

	this.hourBegin = 0;
	this.hourEnd = 4; // max 23
	this.dayBegin = 0;
	this.dayEnd = 6;
	this.calendar = document.getElementById("calendar");



	this.plot = function(){
		this.calendar.style.backgroundColor = "blue";
	}

	this.hourGrid = function(){
		this.hourGrid = document.createElement('TABLE');
		this.hourGrid.style.backgroundColor = "yellow";
		// this.hourGrid.style.height = "50px";
		// this.hourGrid.style.width = "50px";
		this.calendar.appendChild(this.hourGrid);

		for (i=this.hourBegin; i<=this.hourEnd; i++ ){
			var row = document.createElement("tr");
			row.id = +i;
			var cell = document.createElement("td");
			row.innerHTML = i;
			row.appendChild(cell);
			for (var j = this.dayBegin; j < this.dayEnd; j++){
				var cell = document.createElement("td");
				cell.className = "day";
				row.appendChild(cell);
			}

			this.hourGrid.appendChild(row);
		}


	}





	//CONSTRUCTING

	this.plot();
	this.hourGrid();
}




function alertHander(){





	kalendarz = document.getElementById("calendar"); //plotujemy na kalendarzu
	this.qwe = document.createElement("div");
// this.qwe1 = document.createElement("div");


// STYL
	this.qwe.style.position = "absolute";
	this.qwe.style.backgroundColor = "purple";
	this.qwe.style.width = "50px";
	this.qwe.style.height = "50px";
	this.qwe.className = "qwe";
	kalendarz.appendChild(this.qwe);

	//
	// 	this.qwe1.style.position = "absolute";
	// 	this.qwe1.style.backgroundColor = "purple";
	// 	this.qwe1.style.width = "50px";
	// 	this.qwe1.style.height = "50px";
	// 	this.qwe1.className = "qwe";
	// kalendarz.appendChild(this.qwe1);



// OBSŁUGA MÓWMENTU

var selected = null, // Object of the element to be moved
    x_pos = 0, y_pos = 0, // Stores x & y coordinates of the mouse pointer
    x_elem = 0, y_elem = 0; // Stores top, left values (edge) of the element

// Will be called when user starts dragging an element
function _drag_init(elem) {
    // Store the object of the element which needs to be moved
    selected = elem;
    x_elem = x_pos ;//- selected.offsetLeft;
    y_elem = y_pos //- selected.offsetTop;
}

// Will be called when user dragging an element
function _move_elem(e) {
    // x_pos = document.all ? window.event.clientX : e.pageX;
    // y_pos = document.all ? window.event.clientY : e.pageY;
    // if (selected !== null) {
    //     selected.style.left = (x_pos - x_elem) + 'px';
    //     selected.style.top = (y_pos - y_elem) + 'px';
    // }
		//

		// SNAPPING TO GRID
			//GET ALL AVAILABLE Ys
			var allElements = document.getElementsByClassName('day');
			var availableY = [];
			var availableX = [];

			for (var i = 0; i < allElements.length; i++) {
				availableY[i] = allElements[i].offsetTop;
				availableX[i] = allElements[i].offsetLeft;
			}

		x_pos = document.all ? window.event.clientX : e.pageX;
    y_pos = document.all ? window.event.clientY : e.pageY;
    if (selected !== null) {
        selected.style.left = findClosest(availableX,x_pos) + 9 + 'px';
        selected.style.top = findClosest(availableY,y_pos) + 30 + 'px';
    }

}


// Destroy the object when we are done
function _destroy() {
    selected = null;
}

// Bind the functions...
var allAlerts = document.getElementsByClassName('qwe');

for (var i = 0; i < allAlerts.length; i++) {
	allAlerts[i].onmousedown = function () {
			_drag_init(this);
	    return false;
	};
}


function findClosest(dayArray, Pos){
	var distance = Math.abs(Pos - dayArray[0]);
	var closest = dayArray[0];
	for (var i = 1; i < dayArray.length; i++) {
		if (Math.abs(Pos - dayArray[i])<distance)
			closest = dayArray[i];
	}
	return closest;
}


document.onmousemove = _move_elem;
document.onmouseup = _destroy;






}

// DODAĆ REPOSITION POZA EKRANEM screenX
	// DODAĆ TEŻ OBSŁUGĘ TACZA


window.onload = function(){
	var calendar = new Calendar();
	alertHander();
}
