var app = angular.module('catsvsdogs', []);
var socket = io.connect({transports:['polling']});

const images = {init:{i: "https://i.imgur.com/DNFzg3f.png"},//Oscar statue
                A:   {a: "https://i.imgur.com/zx2WG9w.jpg", //Jojo rabbit
                      b: "https://i.imgur.com/W2irJqD.jpg", //Little women
                      c: "https://i.imgur.com/sPR44Fy.jpg", //Parasite
                      d: "https://i.imgur.com/9KI0uQt.jpg", //Marriage story
                      e: "https://i.imgur.com/UadNkSh.jpg"},//Joker
                B:   {a: "https://i.imgur.com/zx2WG9w.jpg", //Jojo rabbit
                      b: "https://i.imgur.com/UadNkSh.jpg", //Joker
                      c: "https://i.imgur.com/W2irJqD.jpg", //Little women
                      d: "https://i.imgur.com/AMFWDbw.jpg", //The irishman
                      e: "https://i.imgur.com/NypSR3a.jpg"},//The 2 popes
                C:   {a: "https://i.imgur.com/RtajjhN.jpg", //Knives out 
                      b: "https://i.imgur.com/sPR44Fy.jpg", //Parasite
                      c: "https://i.imgur.com/XZ5fPPz.jpg", //The lighthouse
                      d: "https://i.imgur.com/ddUurCn.jpg",//1917
                      e: "https://i.imgur.com/9KI0uQt.jpg"},//Marriage story
                D:   {a: "https://i.imgur.com/IpSO4vV.jpg", //Al Pacino
                      b: "https://i.imgur.com/rL2R9Q8.jpg", //Joe Pesci
                      c: "https://i.imgur.com/kfT7h2B.jpg", //Brad Pitt
                      d: "https://i.imgur.com/9hJdz8o.jpg", //Tom Hanks
                      e: "https://i.imgur.com/EBE3aIB.jpg"},//Anthony Hopkins
                E:   {a: "https://i.imgur.com/O3avepO.jpg", //Scarlet Johansson
                      b: "https://i.imgur.com/m5EvbkN.jpg", //Saoirse Ronan
                      c: "https://i.imgur.com/pk9cpWK.jpg", //Charlize Theron
                      d: "https://i.imgur.com/TNestH3.jpg", //Renee Zellweger
                      e: "https://i.imgur.com/NIsGgTG.jpg"},//Cynthia Erivo
                F:   {a: "https://i.imgur.com/TckgA2R.jpg", //Martin Scorsese
                      b: "https://i.imgur.com/Ws5oqwr.jpg", //Todd Phillips
                      c: "https://i.imgur.com/pzKvp3n.jpg", //Sam Mendes
                      d: "https://i.imgur.com/ZeJAc1K.jpg", //Quentin Tarantino
                      e: "https://i.imgur.com/ibFsidU.jpg"} //Bong Joon Ho
                };

app.controller('statsCtrl', function($scope){
  var updateScores = function(){
    socket.on('scores', function (json) {
      data = JSON.parse(json);
      var maxValue = 0;
      var maxKey = 0;
      //x e cheia
      var x;
      var cat;
      var winnerUrl = [0, 0, 0, 0, 0, 0];
      var noUsers = [0, 0, 0, 0, 0, 0];
      var i = 0;
      //var noUsers = 0;

      for (cat in data)
      {
        currentCat = data[cat];
        maxValue = 0;
        maxKey = 0;
        for (x in currentCat) {
            var y = parseInt(currentCat[x] || 0);
            noUsers[i] += y;
            if (y > maxValue) {
              maxKey = x;
              maxValue = y;
            }
        }
        if (maxValue > 0) {
          winnerUrl[i] = images[cat][maxKey];
        } else {
          winnerUrl[i] = images["init"]["i"];
        }
        i++;
      }
      var maxUsers = Math.max(Math.max(...noUsers));

      $scope.$apply(function () {
        $scope.total = maxUsers;
        $scope.url1 = winnerUrl[0];
        $scope.url2 = winnerUrl[1];
        $scope.url3 = winnerUrl[2];
        $scope.url4 = winnerUrl[3];
        $scope.url5 = winnerUrl[4];
        $scope.url6 = winnerUrl[5];
      });
    });
  };

  var init = function(){
    document.body.style.opacity=1;
    updateScores();
  };
  socket.on('message',function(data){
    init();
  });
});