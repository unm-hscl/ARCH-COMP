function val = get(obj, propName)
% get - Retrieve object data from obj
%
% Syntax:  
%    val = get(obj, propName)
%
% Properties:
%    linError - linearization eroor

% Author:       Matthias Althoff
% Written:      30-October-2007
% Last update:  17-May-2011
% Last revision:---

%------------- BEGIN CODE --------------

switch propName
    case 'linError'
        val = obj.linError;  
    case 'jacobians'
        val = obj.jacobians;
otherwise
    error([propName,' is not a valid asset property'])
end

%------------- END OF CODE --------------