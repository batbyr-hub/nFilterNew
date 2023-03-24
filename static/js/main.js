
function prefixOronguud(prefix, numbertype, az) {
    var pre = prefix.toString();
    if(az == 6){
        document.getElementById('digit12').value = pre.substring(0, 2);
        if (numbertype == 7) {
            document.getElementById('digit34').value = pre.substring(2, 4);
        }
        else {
            document.getElementById('digit3').value = pre.substring(2, 3);
            document.getElementById('digit4').value = pre.substring(3, 4);
        }
    }
    else{
        document.getElementById('digit12').value = pre.substring(0, 2);
        document.getElementById('digit34').value = pre.substring(2, 4);
    }
    
}


function loadnumbers(numbertype, az) {
    var prefix = "";
    var number_index = 0;
    //var az = document.getElementById("az").value;
    console.log(az);
    prefix = number(numbertype, az);
    console.log("loadnumbers");
    console.log(prefix);

    $.getJSON("/getnumber?movedown=1&move=" + number_index + "&prefix=" + prefix + "&az=" + az + "&numbertype=" + numbertype, function (data) {
        console.log(data);
        var prefixes = "";
        var empty_couter = Object.keys(data[0]).length;
        console.log(empty_couter);
        var number_index = parseInt(data[1]);
        var az = data[2];
        //console.log(number_index);
        $.each(data[0], function (key, val) {
            prefixes = prefixes + "<div class='number_box Oval1 btn_modal' onclick=\"javascript:order('" + key + "', '"+az+"');\" data-toggle=\"modal\" data-target=\"#myModal\" id=\"myBtn\" style=\"width: 180px; float: left; cursor: pointer; margin-left: 15px; margin-bottom: 3px\">" + val + "</div>";

        });

        if (empty_couter == 0) {

            prefixes = prefixes + "<p class=\"useg\" style=\"text-align: center; margin-top: 10px\">ХАЙСАН ДУГААР ОЛДСОНГҮЙ</p>";

        }
        else {
            empty_couter = 1;
        }

        $("#available_number").html(prefixes);
        $("#available_number").css("display", "block");
        $("#number_prefix").css("display", "none");
        $("#available_move").val(number_index);

    });

}

$(document).ready(function () {
    $("#available_previous").click(function () {
        console.log("available_previous");
        //console.log(prefix);
        var number_index = parseInt($("#available_move").val());
        console.log(number_index);
        var az = document.getElementById("az").value;
        var numbertype = document.getElementById("numbertype").value;
        prefix = number(numbertype, az);

        $.getJSON("/getnumber?move=" + number_index + "&prefix=" + prefix + "&az=" + az + "&numbertype=" + numbertype, function (data) {
            var prefixes = "";
            var empty_couter = Object.keys(data[0]).length;
            var number_index = parseInt(data[1]);
            var az = data[2];
            $.each(data[0], function (key, val) {
                prefixes = prefixes + "<div class='number_box Oval1 btn_modal' onclick=\"javascript:order('" + key + "', '"+az+"');\" data-toggle=\"modal\" data-target=\"#myModal\" id=\"myBtn\" style=\"width: 180px; float: left; cursor: pointer; margin-left: 15px; margin-bottom: 3px\">" + val + "</div>";
            });
            if (empty_couter < 10) {
                var i = 9 - empty_couter;
                if (i == 9) {
                    prefixes = prefixes + "<tr><th onclick=\"alert('Sorry. Number not found!');\" style=\"font-size:21px\">дугаар олдсонгүй</th></tr>";
                    i--;
                }
                for (i; i >= 0; i--) {
                    prefixes = prefixes + "<tr><th  style='font-size:36px'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</th></tr>";
                }
            }

            $("#available_number").html(prefixes);
            $("#available_move").val(number_index);

        });
    });
});

$(document).ready(function () {
    $("#available_next").click(function () {
        console.log("available_next");
        //console.log(prefix);
        var number_index = parseInt($("#available_move").val());
        console.log(number_index);
        var az = document.getElementById("az").value;
        var numbertype = document.getElementById("numbertype").value;
        prefix = number(numbertype, az);
        $.getJSON("/getnumber?movedown=1&move=" + number_index + "&prefix=" + prefix + "&az=" + az + "&numbertype=" + numbertype, function (data) {
            var prefixes = "";
            var empty_couter = Object.keys(data[0]).length;
            var number_index = parseInt(data[1]);
            var az = data[2];
            $.each(data[0], function (key, val) {
                prefixes = prefixes + "<div class='number_box Oval1 btn_modal' onclick=\"javascript:order('" + key + "', '"+az+"');\" data-toggle=\"modal\" data-target=\"#myModal\" id=\"myBtn\" style=\"width: 180px; float: left; cursor: pointer; margin-left: 15px; margin-bottom: 3px\">" + val + "</div>";
            });
            if (empty_couter < 10) {
                var i = 9 - empty_couter;
                if (i == 9) {
                    prefixes = prefixes + "<tr><th onclick=\"alert('Sorry. Number not found!');\" style=\"font-size:21px\">дугаар олдсонгүй</th></tr>";
                    i--;
                }
                for (i; i >= 0; i--) {
                    prefixes = prefixes + "<tr><th  style='font-size:36px'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</th></tr>";
                }
            }

            $("#available_number").html(prefixes);
            $("#available_move").val(number_index);

        });
    });
});

function number(numbertype, az) {
    $("#available_number").html("<p class=\"useg\" style=\"text-align: center; margin-top: 10px\">Loading...</p>"); //"<img src='../images/new_design_images/icons/loader.png' />"
    if (az == 17){
        return document.getElementById('digit12').value + document.getElementById('digit345678').value;
    }
    else{
        if (numbertype == "7") {
            if (az == 6) {
                return document.getElementById('digit12').value + document.getElementById('digit34').value + document.getElementById('digit5').value +
                    document.getElementById('digit6').value + document.getElementById('digit7').value + document.getElementById('digit8').value;
            }
            else {
                return document.getElementById('digit12').value + document.getElementById('digit34').value + document.getElementById('digit5678').value;
            }
        }
        else {
            if (az == 6) {
                return document.getElementById('digit12').value + document.getElementById('digit3').value + document.getElementById('digit4').value +
                    document.getElementById('digit5').value + document.getElementById('digit6').value + document.getElementById('digit7').value + document.getElementById('digit8').value;
            }
            else {
                return document.getElementById('digit12').value + document.getElementById('digit34').value + document.getElementById('digit5678').value;
            }
        }
    }
}

// function num(too) {
//     var out_ser = document.getElementById('show');
//     console.log(out_ser.innerHTML.length);
//     if (too != '-') {
//         if (out_ser.innerHTML.length < 8) {
//             out_ser.innerHTML = out_ser.innerHTML + too;
//         }
//     }
//     else {
//         if (out_ser.innerHTML.length > 0) {
//             out_ser.innerHTML = out_ser.innerHTML.slice(0, -1);
//         }
//     }
//     loadnumbers();
// }

function order(number, luck) {
    var numbertype = document.getElementById("numbertype").value;
    var az = document.getElementById("az").value;
    if(luck == "alt1"){
        az = 5;
    }
    if(luck == "mungu1" || luck == "mungu2" || luck == "mungu3"){
        az = 7;
    }
    if(luck == "hurel1" || luck == "hurel2"){
        az = 9;
    }
    var pathArray = window.location.href.split("/");
    var protocol = pathArray[0];
    var host = pathArray[2];
    var url = protocol + "//" + host + "/numberPrice?number=" + number + "&numbertype=" + numbertype + "&az=" + az;

    console.log(url);
    $.get(url, function (data, status) {

        $("#myModal").html(data);
        $("#myModal").show();

        $("#myModal").find(".close").first().unbind("click");
        $("#myModal").find(".close").first().click(modalCloseClick);

    });

    return false;

    //window.location.href = url;
}

function registr(number, prepost, numbertype, az) {
    var register = document.getElementById("registr").value;
    var re = new RegExp('^[АБВГДЕЁЖЗИЙКЛМНОӨПРСТУҮФХЦЧШЩЬЫЪЭЮЯабвгдеёжзийклмноөпрстуүфхцчшщьыъэюя]{2}[0-9]{8}$');
    if (register == "") {
        registrHooson = "<div class='useg' style=\"margin-left: 40px; color: red\">" + "Регистрийн дугаар заавал оруулна уу" + "</div>";
        $("#registrHooson").html(registrHooson);
    }
    else {
        if (re.test(register)) {
            console.log(register);
            var pathArray = window.location.href.split("/");
            var protocol = pathArray[0];
            var host = pathArray[2];
            var url = protocol + "//" + host + "/zahialga?number=" + number + "&register=" + register + "&prepost=" + prepost + "&numbertype=" + numbertype + "&az=" + az;
            console.log(url);
            window.location.href = url;
        }
        zuvRegistr = "<div class='useg' style=\"margin-left: 40px; color: red\">" + "Зөв регистрийн дугаар оруулна уу" + "</div>";
        zuvhunKrill = "<div class='useg' style=\"margin-left: 40px; color: blue\">" + "Зөвхөн крилл үсэг ашиглана" + "</div>";
        $("#zuvRegistr").html(zuvRegistr);
        $("#zuvhunKrill").html(zuvhunKrill);
    }
}

$(document).ready(function () {

    $(".btn_modal").click(modalBtnClick);

});

function modalBtnClick() {
    var url = $(this).attr("href");
    var final_url = url;
    console.log("modalBtnClick");
    console.log(final_url);

    $.get(url, function (data, status) {

        $("#myModal").html(data);
        $("#myModal").show();

    });

    return false;
}

function move(time) {
    var elem = document.getElementById("myBar");
    var width = 1;
    var id = setInterval(frame, time);

    function frame() {
        if (width >= 100) {
            clearInterval(id);
        } else {
            width++;
            elem.style.width = width + '%';
        }
    }
}
