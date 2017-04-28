function loadHome(){
  window.location = "/";
}
function fixFormatting()
{
  languages = document.getElementsByClassName("languages");
  for (i = 0; i < languages.length; i++){
    userLangs = languages[i];
    langs = userLangs.innerHTML
    userLangs.innerHTML = langs.replace(/'|'/gi, '').replace('[', '').replace(']', '');
  }
  teams = document.getElementsByClassName("teams");
  for(i = 0; i < teams.length; i++){
    userTeams = teams[i];
    unformattedTeams = userTeams.innerHTML
    userTeams.innerHTML = unformattedTeams.replace(/'|'/gi, '').replace('[u', '').replace(']', '').replace(' u', ' ').replace('[','No Teammates');
  }
}
function getUser(row)
{
  cell = row.cells;
  name = cell[0].innerHTML;
  console.log(name);
  window.location = "/userinfo/" + name +"/"+row.rowIndex;
}
