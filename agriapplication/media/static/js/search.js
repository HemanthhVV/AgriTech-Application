const searchQueryField = document.querySelector("#searchQuery");
const appTable = document.querySelector("#actualBlock");
const tableOutput = document.querySelector("#searchBlock");
const tbody = document.querySelector("#tbody");

appTable.style.display = "block";
tableOutput.style.display = "none";
// no_result.style.display = "none";

console.log(searchQueryField);

searchQueryField.addEventListener("keyup", (e) => {
    const searchQuery = e.target.value;
    console.log(searchQuery);

    if (searchQuery.trim().length > 0) {
        tbody.innerHTML = "";
        // paginatorContainer.style.display = "none";

        fetch("search/", {
            body: JSON.stringify({ searchField: searchQuery }),
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": document.querySelector("[name=csrfmiddlewaretoken]").value,
            },
        })
            .then((res) => res.json())
            .then((data) => {
                console.log(data)
                appTable.style.display = "none";
                tableOutput.style.display = "block";
                // no_result.style.display = "none";

                if (data.length === 0) {
                    tableOutput.style.display = "none";
                    // no_result.style.display = "block";
                } else {
                    tableOutput.style.display = "block";
                    // no_result.style.display = "none";

                    data.forEach((img) => {
                        tbody.innerHTML += `
                        <div class="bg-white border border-gray-300 rounded-lg shadow-md flex p-4 mb-4 w-full">
                            <div class="flex-shrink-0 w-2/5">
                                <img src="../media/${img.image}" alt="Uploaded Image" class="w-full h-80 object-cover rounded-md">
                            </div>
                            <div class="ml-4 flex-grow w-3/5 flex flex-col justify-center space-y-2">
                                <h3 class="text-lg font-semibold mb-4">Image Details</h3>
                                <p class="flex items-center">
                                    <strong class="w-40">Uploaded At:</strong>
                                    <span class="ml-2">${img.uploaded_time}</span>
                                </p>
                                <p class="flex items-center">
                                    <strong class="w-40">Latitude:</strong>
                                    <span class="ml-2">${img.latitude}</span>
                                </p>
                                <p class="flex items-center">
                                    <strong class="w-40">Longitude:</strong>
                                    <span class="ml-2">${img.longitude}</span>
                                </p>
                                <p class="flex items-center">
                                    <strong class="w-40">FarmerID:</strong>
                                    <span class="ml-2">${img.farmerID}</span>
                                </p>
                                <p class="flex items-center">
                                    <strong class="w-40">FarmerName:</strong>
                                    <span class="ml-2">${img.farmerName}</span>
                                </p>
                                <p class="flex items-center">
                                    <strong class="w-40">Photo Taken on:</strong>
                                    <span class="ml-2">${img.timeOfPhoto}</span>
                                </p>
                            </div>
                        </div>
                        `;
                    });
                }
            })
            .catch((err) => console.error("Error:", err));
    } else {
        tableOutput.style.display = "none";
        appTable.style.display = "block";
        // paginatorContainer.style.display = "block";
    }
});
