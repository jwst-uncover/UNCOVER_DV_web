var dagcomponentfuncs = (window.dashAgGridComponentFunctions = window.dashAgGridComponentFunctions || {});

dagcomponentfuncs.OverviewPhotLink = function (props) {
    return React.createElement(
        'a',
        {href: '/overviews/phot/' + props.value + '.html'},
        props.value
    );
};

dagcomponentfuncs.OverviewSpecLink = function (props) {
    return React.createElement(
        'a',
        {href: '/overviews/spec' + props.path_extra + '/' + props.value + '.html'},
        props.value
    );
};