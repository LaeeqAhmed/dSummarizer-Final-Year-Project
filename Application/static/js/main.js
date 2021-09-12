const search = document.getElementById('search');
const matchList = document.getElementById('match-list');


const searchmovies = async searchtext => {
    const res = await fetch('http://127.0.0.1:5000/api/names');
    const states = await res.json();

    //get matches through current text input
    let matches = states.filter(state => {
        const regex = new RegExp(`^${searchtext}`,`gi`);
        return state.Name.match(regex);
    });

    if(searchtext.length ===0){
        matches = [];
        matchList.innerHTML = '';
    }
    outputHtml(matches);
};

 const outputHtml = matches =>{

     if(matches.length>0){
         const html = matches.map(match => `
         <div class="search-form-1">
         <div class="w3_search">
         <div class="card card-body mb-1" style="width: 26rem; color:white; background-color:rgba( 153, 153, 153, .5); align-content: center; top: 0%; position: relative; left: -110%">
         <h4 style="text-align: center; font-weight: bold; color: white; background-color: black; font-size:x-large; font-family:Arial;"><a style="color: white;" href="http://127.0.0.1:8000/result/movie/${match.Name}"><b><i>${match.Name}</i></b><span class="text-primary"></span></a></h4>
         </div>
         </div>

         `).join('');

      matchList.innerHTML = html;
     }else if(matches.length==0){

        const html = `
        <div class="search-form-1">
        <div class="w3_search">
        <div class="card card-body mb-1" style="width: 26rem; background-color:rgba( 153, 153, 153, .5); align-content: center; top: -25%; position: relative; left: -110%">
        <h5 style="background-color: red; color: white; text-align: center; font-size:x-large; font-family:Arial;"> MOVIE NOT FOUND <span class="text-primary"></span></h5>
        </div>
        </div>`;
        matchList.innerHTML = html;

     }

 }

search.addEventListener('input', () => searchmovies(search.value));
