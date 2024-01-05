let func = document.getElementById("Function");
func.addEventListener("input", (event) => {
    func_value.innerHTML = event.target.value;
});

let x0 = document.getElementById("x0");
x0.addEventListener("input", (event) => {
    x0_value.innerHTML = event.target.value;
});

let max_iter = document.getElementById("max_iter");
max_iter.addEventListener("input", (event) => {
    max_iter_value.innerHTML = event.target.value;
});

let tolerance = document.getElementById("tolerance");
tolerance.addEventListener("input", (event) => {
    tolerance_value.innerHTML = event.target.value;
});

function fetchData() {
    let func = document.getElementById("Function").value;
    let x0 = document.getElementById("x0").value;
    let max_iter = document.getElementById("max_iter").value;
    let tolerance = document.getElementById("tolerance").value;

    fetch("http://127.0.0.1:5000/calculate", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            func: func,
            x0: x0,
            max_iter: max_iter,
            tolerance: tolerance
        }),
    })
    .then(response => response.json())
    .then(data => {
        // Handle the response data here or modify the sendJsontoPython function
        console.log("Response data:", data);
    })
    .catch(error => {
        console.error("Error fetching data:", error);
    });
}

function drawgif(){} //matplotlib i guess