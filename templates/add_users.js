$(document).ready(function () {
    var counter = 0;

    $("#addrow").on("click", function () {
        var newRow = $("<tr>");
        var cols = "";

        cols += '<td><input type="text" class="form-control" name="firstname' + counter + '"/></td>';
        cols += '<td><input type="text" class="form-control" name="lastname' + counter + '"/></td>';
        cols += '<td><input type="text" class="form-control" name="email' + counter + '"/></td>';
        cols += '<td><input type="checkbox" class="form-control" name="nonharvard' + counter + '"/></td>';
        cols += '<td><input type="checkbox" class="form-control" name="choreographer' + counter + '"/></td>';

        cols += '<td><input type="button" class="ibtnDel btn btn-md btn-danger "  value="Delete"></td>';
        newRow.append(cols);
        $("table.order-list").append(newRow);
        counter++;
    });



    $("table.order-list").on("click", ".ibtnDel", function (event) {
        $(this).closest("tr").remove();       
        counter -= 1
    });


    });