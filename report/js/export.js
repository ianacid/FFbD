let tables = document.getElementsByTagName("table");
let txtexport = [];

for (let table of tables) {
    txtexport[table.id] = "";
    let current = document.getElementById(table.id);
    let rows = current.getElementsByTagName("tr");
    for (let row of rows) {
        let cells = row.getElementsByTagName("td");

        for(let cell of cells) {
            txtexport[table.id] += cell.innerText + '\t';
        }

        txtexport[table.id] += "\n";
    }

    document.getElementById(table.id + "_export_btn").addEventListener("click", () => {
        let a = document.createElement('a');
        a.href = "data:application/octet-stream,"+encodeURIComponent(txtexport[table.id]);
        a.download = table.id + '.txt';
        a.click();
    });
}



