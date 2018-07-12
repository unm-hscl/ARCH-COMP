function [Rfirst,options] = initReach(obj,Rinit,options)
% reach - computes the reachable continuous set for the first time step
%
% Syntax:  
%    [obj,Rfirst,options] = initReach(obj,Rinit,options)
%
% Inputs:
%    obj - linearSys object
%    Rinit - initial reachable set
%    options - options for the computation of the reachable set
%
% Outputs:
%    obj - linearSys object
%    Rfirst - first reachable set 
%    options - options for the computation of the reachable set
%
% Example: 
%
% Other m-files required: none
% Subfunctions: none
% MAT-files required: none
%
% See also: none

% Author: Matthias Althoff
% Written:      07-May-2007 
% Last update:  03-January-2008
%               04-May-2009
%               29-June-2009
%               08-August-2011
%               25-July-2016 (intervalhull replaced by interval)
%               06-April-2017
% Last revision: ---

%------------- BEGIN CODE --------------

% compute exponential matrix
obj = exponential(obj,options);
% compute time interval error (tie)
obj = tie(obj,options);
% compute reachable set due to input
obj = inputSolution(obj,options);
%change the time step
obj.taylor.timeStep=options.timeStep;

%compute reachable set of first time interval
%load data from object structure
eAt=obj.taylor.eAt;
F=obj.taylor.F;
RV=obj.taylor.RV;
inputCorr=obj.taylor.inputCorr;
if iscell(obj.taylor.Rtrans)
    Rtrans=obj.taylor.Rtrans{1};
else
    Rtrans=obj.taylor.Rtrans;
end


%first time step homogeneous solution
Rhom_tp=eAt*Rinit + Rtrans;
if isa(Rinit,'quadZonotope') 
    Rhom=enclose(Rinit,Rhom_tp)+F*zonotope(Rinit)+inputCorr;
elseif isa(Rinit,'zonotopeBundle') 
    Rhom=enclose(Rinit,Rhom_tp)+F*Rinit.Z{1}+inputCorr;
else
    Rhom=enclose(Rinit,Rhom_tp)+F*Rinit+inputCorr;
end

%reduce zonotope
Rhom=reduce(Rhom,options.reductionTechnique,options.zonotopeOrder);
Rhom_tp=reduce(Rhom_tp,options.reductionTechnique,options.zonotopeOrder);
RV=reduce(RV,options.reductionTechnique,options.zonotopeOrder);

%save homogeneous and particulate solution
options.Rhom=Rhom;
options.Rhom_tp=Rhom_tp;
options.Raux=RV;
if (~isfield(options,'linAlg')) || (options.linAlg == 1)
    options.Rpar=interval(RV);
else
    options.Rpar=RV;
end
options.Rtrans=obj.taylor.Rtrans;


%total solution
if isa(Rinit,'mptPolytope')
    %convert zonotopes to polytopes
    Radd=mptPolytope(RV);
    Rtotal=Rhom+Radd;
    Rtotal_tp=Rhom_tp+Radd;
else
    %original computation
    Rtotal=Rhom+RV;
    Rtotal_tp=Rhom_tp+RV;
end

%write results to reachable set struct Rfirst
Rfirst.tp=Rtotal_tp;
Rfirst.ti=Rtotal;


%------------- END OF CODE --------------