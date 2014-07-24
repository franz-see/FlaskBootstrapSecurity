/**
 * Depends on date-1.0-Alpha-1.js
 */

app.factory('todoService', ['$resource', '$filter', function ($resource) {
    var _string_to_date = function(string) {
        return Date.parseExact(string, app.DATE_FORMAT);
    };

    var _date_to_string = function(date) {
        return date.toString(app.DATE_FORMAT);
    };

    var _transform_todo_list_response = function(dataString, headersGetter) {
        var dataObject = angular.fromJson(dataString);
        if (dataObject && dataObject['results']) {
            for (var i = 0; i < dataObject['results'].length; i++) {
                dataObject['results'][i].date = _string_to_date(dataObject['results'][i].date);
            }
        }
        return dataObject;
    };

    var _transform_todo_response = function(dataString, headersGetter) {
        var dataObject = angular.fromJson(dataString);
        if (dataObject && dataObject.date) {
            dataObject.date = _string_to_date(dataObject.date);
        }
        return dataObject;
    };
    
    var _transform_todo_request = function(dataObject, headersGetter) {
        if (dataObject && dataObject.date) {
            dataObject.date = _date_to_string(dataObject.date);
        }
        return angular.toJson(dataObject);
    };
    
    return $resource('/api/todo/:id', {}, {
        save:  { method:'POST', transformRequest:_transform_todo_request,       transformResponse:_transform_todo_response },
        query: { method: 'GET', transformResponse:_transform_todo_list_response }
    });
}]);