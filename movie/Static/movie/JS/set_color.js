function componentToHex(c) {
    var hex = c.toString(16);
    return hex.length == 1 ? "0" + hex : hex;
}

function rgbToHex(r, g, b) {
    return "#" + componentToHex(r) + componentToHex(g) + componentToHex(b);
}

function hexToRgb(hex) {
        var result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);
        return result ? {
            r: parseInt(result[1], 16),
            g: parseInt(result[2], 16),
            b: parseInt(result[3], 16)
    } : null;
}

var r_global = 0
var g_global = 0
var b_global = 0
bg_img = document.getElementById("bg_image").src;
img2 = document.getElementById("bg_image")

function Gradient(){
    width = document.defaultView.innerWidth;
    if(width >= "1000"){
        gradient = "linear-gradient(to right, rgba("+r_global+","+g_global+","+b_global+",1), rgba("+r_global+","+g_global+","+b_global+",0)), linear-gradient(to top, rgba("+r_global+","+g_global+","+b_global+",1), rgba("+r_global+","+g_global+","+b_global+",0))";
    }
    else{
        gradient = "linear-gradient(to top, rgba("+r_global+","+g_global+","+b_global+",1), rgba("+r_global+","+g_global+","+b_global+",0))";
    }
    document.getElementById("bg_img").style.backgroundImage = gradient+',url('+bg_img+')';
}

img2 = document.getElementById("Poster_img");
img2.setAttribute('crossOrigin', '');

img2.onload = function() {
    var img = img2.cloneNode(true);
    width = this.width;
    height = this.height;
    canvas = document.createElement('canvas');
    canvas.width = width; 
    canvas.height = height;
    ctx = canvas.getContext("2d");
    ctx.drawImage(img,0,0,canvas.width,canvas.height);
    
    var image_data = ctx.getImageData(0,0,canvas.width,canvas.height);
    var pix = image_data.data;
    var hex_Values = {};
    for (var i = 0, n = pix.length; i < n; i += 4) {
        var r = pix[i];
        var d = r%25
        if (d<13){
            r = r-d;
        }
        else {
            r = r-(25-d);
        }
        var g = pix[i+1];
        var d = g%25
        if (d<13){
            g = g-d;
        }
        else {
            g = g-(25-d);
        }
        var b = pix[i+2];
        var d = b%25
        if (d<13){
            b = b-d;
        }
        else {
            b = b-(25-d);
        }
        if(r!=g || r!=b || g!=b){
            var values = rgbToHex(r,g,b);
            if (values in hex_Values){
                hex_Values[values] += 1;
            }
            else{
                hex_Values[values] = 1;
            }
        }
    }
    
    maxValue = 0;
    maxKey = "";
    for(let value in hex_Values){
        if (hex_Values[value] > maxValue){
            maxValue = hex_Values[value];
            maxKey = value;
        }
    }
    if (Object.keys(hex_Values).length === 0) {
        hex_Values["#000000"] = 1;
    }
    
    
    mainColor_RGB = hexToRgb(maxKey);
    if(mainColor_RGB){
        r = mainColor_RGB.r;
        g = mainColor_RGB.g;
        b = mainColor_RGB.b;
    }
    else{
        r = 0;
        g = 0;
        b = 0;
    }
    
    var mainColor = rgbToHex(r,g,b);
    
    if (r<85 && g<85 && b<85){
        var backgroundColor = rgbToHex(r,g,b);
        var textColor = rgbToHex(Math.round((r+255)/2),Math.round((g+255)/2),Math.round((b+255)/2));
        var lightColor = textColor;
        var darkColor = backgroundColor;
    }
    else if(r>170 && g>170 && b>170){
        var backgroundColor = rgbToHex(Math.round((r+255)/2),Math.round((g+255)/2),Math.round((b+255)/2))
        var textColor = rgbToHex(Math.round((r)/2),Math.round((g)/2),Math.round((b)/2));
        var lightColor = backgroundColor;
        var darkColor = textColor;
    }
    else{
        var textColor = rgbToHex(Math.round((r+255)/2),Math.round((g+255)/2),Math.round((b+255)/2));
        var backgroundColor = rgbToHex(Math.round(r/3),Math.round(g/3),Math.round(b/3));
        var lightColor = textColor;
        var darkColor = backgroundColor;
    }
    
    bg_color = hexToRgb(backgroundColor);
    r_global = bg_color.r;
    g_global = bg_color.g;
    b_global = bg_color.b;
    document.documentElement.style.setProperty('--text-color', textColor);
    document.documentElement.style.setProperty('--bg-color', backgroundColor);
    document.documentElement.style.setProperty('--light-color', lightColor);
    document.documentElement.style.setProperty('--dark-color', darkColor);
    
    width = document.defaultView.innerWidth
    if(width >= "1000"){
        gradient = "linear-gradient(to right, rgba("+r_global+","+g_global+","+b_global+",1), rgba("+r_global+","+g_global+","+b_global+",0)),linear-gradient(to top, rgba("+r_global+","+g_global+","+b_global+",1), rgba("+r_global+","+g_global+","+b_global+",0))";
    }
    else{
        gradient = "linear-gradient(to top, rgba("+r_global+","+g_global+","+b_global+",1), rgba("+r_global+","+g_global+","+b_global+",0))";
    }
    document.getElementById("bg_img").style.backgroundImage = gradient+',url('+bg_img+')';

    document.body.style.background = textColor;

}