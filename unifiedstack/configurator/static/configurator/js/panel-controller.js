	
        /*
        angular.module("SampleUIApp", ["ngResource"]).config(
            function ($routeProvider) {
                $routeProvider.when('/', {controller: panelController, templateUrl: 'index.html'}).otherwise({redirectTo: '/'});
            };
        )
        */
        function panelController($scope){
            $scope.affirmative = true;
            $scope.is_fi_settings = true;
	    $scope.panels = [
		{panel_title: "Title 1", panel_style: "panel-primary", fields: [{"Field1":"field1", "field2":"field2"}]},
		{panel_title: "Title 2", panel_style: "panel-default", fields: [{"field1": "funny"}]}
	    ]
	}
        
	/*
	$scopte.add_panel = function() {
	    $scope.panels.push({
		panel_title: "",
		panel_style: "",
		panel_fields: []
	    });
	}
	$scope.panel_colors = [""]
	*/
