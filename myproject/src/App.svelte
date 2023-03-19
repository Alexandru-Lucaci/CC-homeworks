<script>
  import { each } from "svelte/internal";

  	// export let name;
	let firstName = 'John';
	let lastName = 'Doe';
	let table = '';
	let viewAllTable = 'none';
	let viewFilterButton = 'none';
	let viewFindButton = 'none';
	let viewAddButton = 'none';
	let viewDelButton = 'none';
	let idFind = '';
	let findData = new Map();
	
	let filterDataName = '';
	let filterDataType = '';
	let filterDataFilm = '';
	let filterDataId = '';
	var apiData = new Map();

	let addDataName = '';
	let addDataType = '';
	let addDataFilm = '';
	let addDataCheck = 'on';	

	let delDataName = '';
	let delDataId = '';
	
	let beltColour='black';
	const handle_click = () => {
		beltColour = 'orange';
	};
	const handle_input = (event) => {
		beltColour = event.target.value;
	};
	const seeAllinserts = () => {
		viewAddButton = 'none';
		viewFilterButton = 'none';
		viewFindButton = 'none';
		viewDelButton = 'none';
		if (viewAllTable == 'none') {
			viewAllTable = 'block';
		} else {
			viewAllTable = 'none';
		}
		// viewAllTable = 'visible';
		fetch("http://localhost:5000/films")
		.then(response => response.json())
		.then(data => {
				// for (let [key,value] of Object.entries(data)) {
				// 	table+=`<tr><th scope="row">${key}</th><td>${value.name}</td><td>${value.type}</td><td>${value.genre}</td></tr>`;
				// }
				console.log(table)
			apiData=data;
			// check if the data is empty

			console.log(apiData)
			console.log(table)
		}).catch(error => {
			console.log(error);
			return [];
		// generate a table with data
  });
	};
	const filterbtnPressed = () => {
		viewAddButton = 'none';
		viewAllTable = 'none';
		viewFindButton = 'none';
		viewDelButton = 'none';
		viewFilterButton = 'block';


	};
	const findAfilm = () => {
		viewAddButton = 'none';
		viewDelButton = 'none';
		viewAllTable = 'none';
		viewFilterButton = 'none';
		viewFindButton = 'block';

	};
	const handFindId = (event) => {
		idFind = event.target.value;
		console.log(idFind);
		fetch("http://localhost:5000/"+idFind)
		.then(response => response.json())
		.then(data => {
				// for (let [key,value] of Object.entries(data)) {
				// 	table+=`<tr><th scope="row">${key}</th><td>${value.name}</td><td>${value.type}</td><td>${value.genre}</td></tr>`;
				// }
				console.log(table)
			findData=data;
			// check if the data is empty

			console.log(findData)
			// console.log(table)
		}).catch(error => {
			console.log(error);
			return [];
		});
	};


	const handFilterName = (event) => {
		filterDataName = event.target.value;
		console.log(filterDataName);
		var stringPar =""
		if(filterDataName != ''){
			stringPar += "name="+filterDataName+"&";
		}
		if(filterDataType != ''){
			stringPar += "type="+filterDataType+"&";
		}
		if(filterDataFilm != ''){
			stringPar += "film="+filterDataFilm+"&";
		}
		// remove the last &
		stringPar = stringPar.slice(0, -1);
		fetch("http://localhost:5000/get/"+stringPar)
		.then(response => response.json())
		.then(data => {
				// for (let [key,value] of Object.entries(data)) {
				// 	table+=`<tr><th scope="row">${key}</th><td>${value.name}</td><td>${value.type}</td><td>${value.genre}</td></tr>`;
				// }
				console.log(table)
			findData=data;
			// check if the data is empty

			console.log(findData)
			// console.log(table)
		}).catch(error => {
			console.log(error);
			return [];
		});
	};
	const handFilterType = (event) => {
		filterDataType = event.target.value;
		console.log(filterDataType);
		var stringPar =""
		if(filterDataName != ''){
			stringPar += "name="+filterDataName+"&";
		}
		if(filterDataType != ''){
			stringPar += "type="+filterDataType+"&";
		}
		if(filterDataFilm != ''){
			stringPar += "film="+filterDataFilm+"&";
		}
		stringPar = stringPar.slice(0, -1);
		fetch("http://localhost:5000/get/"+stringPar)
		.then(response => response.json())
		.then(data => {
				// for (let [key,value] of Object.entries(data)) {
				// 	table+=`<tr><th scope="row">${key}</th><td>${value.name}</td><td>${value.type}</td><td>${value.genre}</td></tr>`;
				// }
				console.log(table)
			findData=data;
			// check if the data is empty

			console.log(findData)
			// console.log(table)
		}).catch(error => {
			console.log(error);
			return [];
		});
	};
	const handFilterFilm = (event) => {
		filterDataFilm = event.target.value;
		console.log(filterDataFilm);
		var stringPar =""
		if(filterDataName != ''){
			stringPar += "name="+filterDataName+"&";
		}
		if(filterDataType != ''){
			stringPar += "type="+filterDataType+"&";
		}
		if(filterDataFilm != ''){
			stringPar += "film="+filterDataFilm+"&";
		}
		stringPar = stringPar.slice(0, -1);
		fetch("http://localhost:5000/get/"+stringPar)
		.then(response => response.json())
		.then(data => {
				// for (let [key,value] of Object.entries(data)) {
				// 	table+=`<tr><th scope="row">${key}</th><td>${value.name}</td><td>${value.type}</td><td>${value.genre}</td></tr>`;
				// }
				console.log(table)
			findData=data;
			// check if the data is empty

			console.log(findData)
			// console.log(table)
		}).catch(error => {
			console.log(error);
			return [];
		});
	};

	const addBtnPressed = () => {
		viewAllTable = 'none';
		viewFilterButton = 'none';
		viewFindButton = 'none';
		viewDelButton = 'none';
		viewAddButton = 'block';
	};
	const delBtnPressed = () => {
		viewAllTable = 'none';
		viewFilterButton = 'none';
		viewFindButton = 'none';
		viewDelButton = 'block';
		viewAddButton = 'none';
	};
	const tryAddFilm = () => {
		var stringPar =""
		if(addDataName != ''){
			stringPar += "name="+addDataName+"&";
		}
		if(addDataType != ''){
			stringPar += "type="+addDataType+"&";
		}
		if(addDataFilm != ''){
			stringPar += "film="+addDataFilm+"&";
		}
		stringPar = stringPar.slice(0, -1);
		fetch("http://localhost:5000/post/?"+stringPar,{method : 'POST'})
		.then(response => response.json())
		.then(data => {
				// for (let [key,value] of Object.entries(data)) {
				// 	table+=`<tr><th scope="row">${key}</th><td>${value.name}</td><td>${value.type}</td><td>${value.genre}</td></tr>`;
				// }
				console.log(table)
			findData=data;
			// check if the data is empty

			console.log(findData)
			// console.log(table)
		}).catch(error => {
			console.log(error);
			return [];
		});
	};

	const handAddName = (event) => {
		addDataName = event.target.value;
		console.log(addDataName);
	};
	const handAddType = (event) => {
		addDataType = event.target.value;
		console.log(addDataType);
	};
	const handAddFilm = (event) => {
		addDataFilm = event.target.value;
		console.log(addDataFilm);
	};
	const handAddCheck  = (event) => {
		if (event.target.checked) {
			addDataCheck = true;
		} else {
			addDataCheck = false;
		}
		// addDataCheck = event.target.value;
		console.log(addDataCheck);
	};
	const handDelName = (event) => {
		delDataName = event.target.value;
		console.log(delDataName);
	};
	const tryDelFilm = () => {
		var stringPar =""
		if(delDataName != ''){
			stringPar += "name="+delDataName+"&";
		}
		stringPar = stringPar.slice(0, -1);
		fetch("http://localhost:5000/delete/?"+stringPar,{method : 'DELETE'})
		.then(response => response.json())
		.then(data => {
				// for (let [key,value] of Object.entries(data)) {
				// 	table+=`<tr><th scope="row">${key}</th><td>${value.name}</td><td>${value.type}</td><td>${value.genre}</td></tr>`;
				// }
				console.log(table)
			findData=data;
			// check if the data is empty

			console.log(findData)
			// console.log(table)
		}).catch(error => {
			console.log(error);
			return [];
		});
	};

</script>

<main>
	<nav class="navbar navbar-light bg-light">
		<form class="form-inline">
		  <button class="btn btn-outline-success" type="button" on:click={seeAllinserts}>View all button</button>
		  <button class="btn btn-sm btn-outline-secondary" type="button" on:click={findAfilm}>Find button</button>
		  <button class="btn btn-sm btn-outline-secondary" type="button" on:click={filterbtnPressed}>Filter button</button>
		  <button class="btn btn-sm btn-outline-secondary" type="button" on:click={addBtnPressed}>Add button</button>
		  <button class="btn btn-sm btn-outline-secondary" type="button">Update button</button>
		  <button class="btn btn-sm btn-outline-secondary" type="button" on:click={delBtnPressed}>Delete button</button>
		</form>
	  </nav>
	  
	<!-- <h1>Hello {name}!</h1>
	<p>Hello test</p>
	<p style="color: {beltColour}">My belt colour is {beltColour}</p>
	<button on:click={handle_click}>update belt color</button>
	<input type="text" on:input={handle_input} value={beltColour}> 
	<input type="text" bind:value={beltColour}> -->

	<table class="table table-dark table-hover" style="display:{viewAllTable} ;"><thead><tr><th scope="col">#</th><th scope="col">Name of the film</th><th scope="col">Type of the film</th><th scope="col">Film genre</th></tr></thead><tbody>
	{#each Object.entries(apiData) as [key, value]}
		<tr scope="row">
			{#if key !='#'}
				<td>{key}</td>
				<td>{value.name}</td>
				<td>{value.type}</td>
				<td>{value.film}</td>
			{/if}
		
		</tr>
	{/each}
	</tbody></table>
	
	<div class="container-fluid p-5 bg-primary text-white text-center" style="display: {viewFindButton};">
		<h1>Find A film</h1>
		<p>Here we can input a film</p>
	</div>
	<form action="" method="" style="display: {viewFindButton};">
		<div class="mb-3">
		<label class="form-label" for="exampleInputNameFilm">Id</label>
		<input class="form-control" id="exampleInputNameFilm" name="name" type="text" on:input={handFindId}/>
		</div>
		<table class="table table-dark table-hover" style="display:{viewFindButton} ;"><thead><tr><th scope="col">#</th><th scope="col">Name of the film</th><th scope="col">Type of the film</th><th scope="col">Film genre</th></tr></thead><tbody>
		<tr scope ="row">
			<td>{idFind}</td>
			<td>{findData.name}</td>
			<td>{findData.type}</td>
			<td>{findData.film}</td>
			</tr>
		</tbody></table>
	</form>
	
	<div class="container-fluid p-5 bg-primary text-white text-center" style="display: {viewFilterButton};">
		<h1>Filter films</h1>
		<p>Here we can input a film</p>
	</div>
	<form action="" method="" style="display: {viewFilterButton};">
		<div class="mb-3">
		<label class="form-label" for="exampleInputNameFilm">Name</label>
		<input class="form-control" id="exampleInputNameFilm" name="name" type="text" on:input={handFilterName}>
		<label class="form-label" for="exampleInputNameFilm">Type</label>
		<input class="form-control" id="exampleInputNameFilm" name="name" type="text" on:input={handFilterType}/>
		<label class="form-label" for="exampleInputNameFilm">Film</label>
		<input class="form-control" id="exampleInputNameFilm" name="name" type="text" on:input={handFilterFilm}/>
		</div>
		<table class="table table-dark table-hover" style="display:{viewFilterButton} ;"><thead><tr><th scope="col">#</th><th scope="col">Name of the film</th><th scope="col">Type of the film</th><th scope="col">Film genre</th></tr></thead><tbody>
			{#each Object.entries(findData) as [key, value]}
				<tr scope="row">
					{#if key !='#'}
						<td>{key}</td>
						<td>{value.name}</td>
						<td>{value.type}</td>
						<td>{value.film}</td>
					{/if}
				
				</tr>
			{/each}
			</tbody></table>
	</form>
	<div style="display:{viewAddButton}">
		<div class="container-fluid p-5 bg-primary text-white text-center">
			<h1>Input a film</h1>
			<p>Here we can input a film</p>
		</div>
		<form action="" method="post">
			<div class="mb-3">
				<label class="form-label" for="exampleInputNameFilm" >Name of the film</label>
				<input class="form-control" id="exampleInputNameFilm" name="name" type="text" on:input={handAddName}/>
			</div>
			<div class="mb-3">
				<label class="form-label" for="exampleInputType">
				  Type of the film
				</label>
				<input class="form-control" id="exampleInputType" name="type" type="text" on:input={handAddType}/>
			</div>
		<div class="mb-3">
			<label class="form-label" for="exampleInputType">Film genre </label>
			<input class="form-control" id="exampleInputType" name="film" type="text" on:input={handAddFilm}/>
		</div>
		<div class="mb-3 form-check">
			<input class="form-check-input" id="exampleCheck1" name="checked" type="checkbox" on:input={handAddCheck}/>
			<label class="form-check-label" for="exampleCheck1">Check if already exists</label>
		</div>
		<button class="btn btn-primary" on:click={tryAddFilm}>Introdu</button>
		</form>
	</div>

	<div style="display:{viewDelButton}">
		<div class="container-fluid p-5 bg-primary text-white text-center">
			<h1>Deletre a film</h1>
			<p>Here we can input a film</p>
			</div>
		<form action="" method="DELETE">
			<div class="mb-3">
				<label class="form-label" for="exampleInputNameFilm" >Name of the film</label>
				<input class="form-control" id="exampleInputNameFilm" name="name" type="text" on:input={handDelName}/>
			</div>
			<button class="btn btn-primary" on:click={tryDelFilm}>Introdu</button>
		</form>
	</div>
	
</main>

<style>
	main {
		/* text-align: center; */
		padding: 1em;
		max-width: 240px;
		margin: 0 auto;
	}

	h1 {
		color: #ff3e00;
		text-transform: uppercase;
		font-size: 4em;
		font-weight: 100;
	}

	@media (min-width: 640px) {
		main {
			max-width: none;
		}
	}
</style>