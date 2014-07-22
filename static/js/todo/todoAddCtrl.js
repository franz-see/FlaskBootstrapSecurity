app.controller('TodoAddCtrl', ['$scope', '$modal', '$log', function ($scope, $modal, $log) {
    $scope.dt = new Date();
    $scope.openDatePicker = function ($event) {
        $event.preventDefault();
        $event.stopPropagation();

        $scope.opened = true;
    };

    $scope.dateOptions = {
        formatYear: 'yy',
        startingDay: 1
    };

    $scope.format = app.dateFormat;
}]);
