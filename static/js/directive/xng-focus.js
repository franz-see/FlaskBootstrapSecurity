app.directive('xngFocus', function($timeout) {
  return {
    scope: { trigger: '@xngFocus' },
    link: function(scope, element) {
      scope.$watch('trigger', function(value) {
        if(value === "true") {
          // console.log('trigger',value);
          $timeout(function() {
            element[0].focus();
          });
        }
      });
    }
  };
});
