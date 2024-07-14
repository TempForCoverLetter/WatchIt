document.getElementById("watch-btn").addEventListener("click",async () =>{
    document.getElementById("watch-btn").disabled = true;
    document.getElementById("watch-video").innerHTML="";
    let se = document.getElementById("season_select");
    let ep;
    let title=document.getElementsByTagName("h5")[0].innerText;
    if(se){
        se=se.value;
        ep = document.getElementById("episode_select").value;
        if(se == "Choose" || ep == "Choose")
        {
            document.getElementById("watch-video").innerHTML='<div class="center-alert"><div class="alert alert-danger" role="alert">No season or episode have been selected</div></div>';
            document.getElementById("watch-btn").disabled = false;
            return;
        }
        if(parseInt(se)==0){
            se =" special";
            ep="";}
        else{
            if(parseInt(se)<=9)
                se = " S0"+se;
            else
                se = " S"+se;
            if(parseInt(ep)<=9)
                ep = "E0"+ep;
            else
                ep = "E"+ep;}
        
        title = title.substring(title.indexOf(':') + 2)+se+ep
    }
    else
    {
        let year=document.getElementsByTagName("h5")[3].innerText
        let index = year.indexOf(':') + 2
        title=title.substring(title.indexOf(':') + 2)+" "+year.substring(index,index+4);
    }
    document.getElementById("loader").hidden = false;
    let response = await fetch("/get_torrent/"+title);
    let torrentId = await response.text();
    if(torrentId == "")
    {
        document.getElementById("watch-video").innerHTML='<div class="center-alert"><div class="alert alert-danger" role="alert">The providers have no link</div></div>';
        document.getElementById("loader").hidden = true;
        document.getElementById("watch-btn").disabled = false;
        return;
    }
    let response_lang = await fetch("/get_lang");
    let user_lang = await response_lang.text();
    let imdb;
    if(se)
    {
        let response = await fetch(("/get_imdb/"+(/[^/]*$/.exec(window.location.href)[0])+"/"+parseInt(se.slice(2))+'/'+parseInt(ep.slice(1))));
        imdb = await response.text();
    }
    else
    {
        imdb = document.getElementById("watch-btn").dataset.imdbid;
    }
    if(Math.random() < 0.7)
    {
        document.getElementById("watch-video").innerHTML = '<iframe src="https://streamtorrent.onrender.com/?imdb_id='+imdb+'&torrent='+torrentId+'" frameborder="0" allowfullscreen webkitallowfullscreen="true" mozallowfullscreen="true" oallowfullscreen="true" msallowfullscreen="true"/>';
    }
    else{
        document.getElementById("watch-video").innerHTML = '<iframe src="https://dawn-butterfly-7836.fly.dev/?imdb_id='+imdb+'&torrent='+torrentId+'" frameborder="0" allowfullscreen webkitallowfullscreen="true" mozallowfullscreen="true" oallowfullscreen="true" msallowfullscreen="true"/>';
    }
    //magnet: torrentId,
    //torrentUrl: "https://my-flask-app-gad1001.vercel.app/get_torrent/"+title,
    /*window.webtor = window.webtor || [];
        window.webtor.push({
            id: 'watch-video',
            torrentUrl: torrentId,
            title: title,
            imdbId: imdb,
            poster: window.getComputedStyle(document.getElementsByClassName("background-poster")[0], false).backgroundImage.slice(73,-2),
            lang: user_lang.slice(0,2),
            userLang: user_lang.slice(0,2),
            features: {
                autoSubtitles:true,
                embed: false,
                settings: false,
            },
        });*/
    
    document.getElementById("loader").hidden = true;
    document.getElementById("watch-btn").disabled = false;
});
