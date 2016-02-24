app.controller('HomeCtrl', function($rootScope, $location)
{
   $rootScope.activetab = $location.path();
});
 
app.controller('ClienteCtrl', function($rootScope, $location)
{
   $rootScope.activetab = $location.path();
});
 
app.controller('ContatoCtrl', function($rootScope, $location)
{
   $rootScope.activetab = $location.path();
});