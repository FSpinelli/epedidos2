var app = angular.module('app',['ngRoute', 'ui.mask']);
var baseViews = '/static/app/views';
app.config(function($routeProvider, $interpolateProvider)
{

   $interpolateProvider.startSymbol('[[');
   $interpolateProvider.endSymbol(']]');
 
   $routeProvider
 
   .when('/', {
      templateUrl : baseViews+'/home.html',
      controller     : 'HomeCtrl',
   })

   .when('/clientes', {
      templateUrl : baseViews+'/clientes/index.html',
      controller  : 'ClienteCtrl',
   })
 
   .when('/clientes/cadastrar', {
      templateUrl : baseViews+'/clientes/form.html',
      controller  : 'ClienteCtrl',
   })
 
   .when('/contato', {
      templateUrl : baseViews+'/contato.html',
      controller  : 'ContatoCtrl',
   })
 
   .otherwise ({ redirectTo: '/' });
});