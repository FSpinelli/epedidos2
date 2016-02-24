var app = angular.module('app',['ngRoute']);
var baseViews = '/static/app/views';
app.config(function($routeProvider, $interpolateProvider)
{

   $interpolateProvider.startSymbol('[[');
   $interpolateProvider.endSymbol(']]');
 
   $routeProvider
 
   // para a rota '/', carregaremos o template home.html e o controller 'HomeCtrl'
   .when('/', {
      templateUrl : baseViews+'/home.html',
      controller     : 'HomeCtrl',
   })
 
   // para a rota '/sobre', carregaremos o template sobre.html e o controller 'SobreCtrl'
   .when('/clientes/cadastrar', {
      templateUrl : baseViews+'/clientes/form.html',
      controller  : 'ClienteCtrl',
   })
 
   // para a rota '/contato', carregaremos o template contato.html e o controller 'ContatoCtrl'
   .when('/contato', {
      templateUrl : baseViews+'/contato.html',
      controller  : 'ContatoCtrl',
   })
 
   // caso não seja nenhum desses, redirecione para a rota '/'
   .otherwise ({ redirectTo: '/' });
});