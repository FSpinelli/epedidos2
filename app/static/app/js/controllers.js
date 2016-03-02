app.controller('HomeCtrl', function($rootScope, $location)
{
   $rootScope.activetab = $location.path();
});
 
app.controller('ClienteCtrl', function($rootScope, $location, $scope, $http, $window)
{
   	$rootScope.activetab = $location.path();

    $scope.save = function (e) {
	    $http({
	        method : "POST",
	        url: 'http://127.0.0.1:8000/api/clientes/',
	        headers: {'Content-Type': 'application/x-www-form-urlencoded'},
	        data: $.param($scope.formData)
	    }).then(function mySucces(response) {
			// for (var key in response.data) {
			//   console.log(key + " -> " + response.data[key]);
			// }
			if(response.data == 200){
				alert('Cliente cadastrado com sucesso.');
				$window.location.href = '#/clientes';
			}
	    }, function myError(response) {
	        alert('Ops! Ocorreu um erro. Tente mais tarde.');
	    });
    }; 
});
 
app.controller('ContatoCtrl', function($rootScope, $location)
{
   $rootScope.activetab = $location.path();
});