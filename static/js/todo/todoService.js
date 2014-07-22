app.factory('todoService', ['$resource', function ($resource) {
    return $resource('/api/todo/:id', {}, {
      query: { method: 'GET' }
    });
}]);