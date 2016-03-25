function formatPoints(points) {
    result = "";
    for (var i = 0; i < points.length; i++) {
        result += "(" + String(points[i][0]) + "," + String(points[i][1]) + ")";
        if (i < points.length - 1) {
          result += " ";
        }
    }
    return result;
}

function encodePoints(input) {
    var points = [];
    input = input.replace(" ", "");
    input = input.replace(")", ") ");
    var components = input.split(" ");
    for (var i = 0; i < components.length; i++) {
        if(components[i].trim() == "") {
            continue;
        }
        point = [0, 0];
        point[0] = Number(stringBetweenString(components[i], "(", ",").trim());
        point[1] = Number(stringBetweenString(components[i], ",", ")").trim());
        points.push(point);
    }
    return points;
}

function stringBetweenString(input, string1, string2) {
    return input.substring(input.indexOf(string1) + 1, input.indexOf(string2));
}

String.prototype.hashCode = function(){
    var hash = 0;
    if (this.length == 0) return hash;
    for (var i = 0; i < this.length; i++) {
        var character = this.charCodeAt(i);
        hash = ((hash<<5)-hash)+character;
        hash = hash & hash;
    }
    return Math.abs(hash);
}
