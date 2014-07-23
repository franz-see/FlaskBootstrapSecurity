app.controller('TodoModalCtrl', ['$scope', '$modal', function ($scope, $modal) {
    $scope.format = app.dateFormat;
    $scope.openModal = function (size) {

        var modalInstance = $modal.open({
            templateUrl: 'todoAddCtrl.html',
            controller: function ($scope, $modalInstance) {
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

                $scope.ok = function () {
                    $modalInstance.close();
                };

                $scope.cancel = function () {
                    $modalInstance.dismiss('cancel');
                };
            },
            size: size,
            resolve: {
            }
        });

        modalInstance.result.then(function (selectedItem) {
        }, function () {
        });
    };
}]);
