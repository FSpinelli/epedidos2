app.controller('HomeCtrl', function($rootScope, $location)
{
   $rootScope.activetab = $location.path();
});
 
app.controller('ClienteCtrl', function($rootScope, $location, $scope, $http)
{
   $rootScope.activetab = $location.path();

    $scope.save = function (e) {
		// $http({
		//     method: 'POST',
		//     url: 'http://127.0.0.1:8000/api/clientes/',
		//     headers: {'Content-Type': 'application/x-www-form-urlencoded'},
		//     transformRequest: function(obj) {
		//         var str = [];
		//         for(var p in obj)
		//         str.push(encodeURIComponent(p) + "=" + encodeURIComponent(obj[p]));
		//         return str.join("&");
		//     },
		//     data: {username: $scope.userName, password: $scope.password}
		// }).success(function (res) {
		// 	console.log(res);
		// });


	 //    $http({
	 //        method : "POST",
	 //        url: 'http://127.0.0.1:8000/api/clientes/',
	 //        headers: {'Content-Type': 'application/x-www-form-urlencoded'},
	 //    }).then(function mySucces(response) {
	 //        $scope.myWelcome = response.data;
	 //    }, function myError(response) {
	 //        $scope.myWelcome = response.statusText;
	 //    });


    }; 

});
 
app.controller('ContatoCtrl', function($rootScope, $location)
{
   $rootScope.activetab = $location.path();
});