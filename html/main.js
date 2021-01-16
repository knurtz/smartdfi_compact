function updateFont(line) {

  var newFont = document.getElementById(line+"-font").value;

  switch(newFont) {

    case 'B':
      document.getElementById(line+"-left").style.fontWeight = "bold";
      document.getElementById(line+"-right").style.fontWeight = "bold";
      break;

    default:
      document.getElementById(line+"-left").style.fontWeight = "normal";
      document.getElementById(line+"-right").style.fontWeight = "normal";
      break;
  }

}

function hideSecondField(line) {

  document.getElementById(line+"-right").style.width = "0%"
  document.getElementById(line+"-left").style.width = "100%";
  document.getElementById(line+"-right").style.display = "none";

}


function showSecondField(line) {

  document.getElementById(line+"-right").style.width = "48%"
  document.getElementById(line+"-left").style.width = "48%";
  document.getElementById(line+"-right").style.display = "inline";

  document.getElementById(line+"-left").style.textAlign = "left";

}

function updateAlign(line) {

  var newAlign = document.getElementById(line+"-align").value;

  switch(newAlign) {

    case 'L':
    hideSecondField(line);
    document.getElementById(line+"-left").style.textAlign = "left";
    break;

    case 'M':
    hideSecondField(line);
    document.getElementById(line+"-left").style.textAlign = "center";
    break;

    case 'R':
    hideSecondField(line);
    document.getElementById(line+"-left").style.textAlign = "right";
    break;

    case 'X':
    showSecondField(line);
    break;

  }

}
