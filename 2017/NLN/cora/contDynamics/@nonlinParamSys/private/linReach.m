function [Rti,RtpEnh,nr,options] = linReach(obj,options,Rstart,recur)
% linReach - computes the reachable set after linearazation and returns if
% the initial set has to be split in order to control the linearization
% error
%
% Syntax:  
%    [Rti,Rtp,split,options] = linReach(obj,options,Rinit)
%
% Inputs:
%    obj - nonlinear system object
%    options - options struct
%    Rinit - initial reachable set
%
% Outputs:
%    Rti - reachable set for time interval
%    Rti - reachable set for time point
%    split - boolean value returning if initial set has to be split
%    options - options struct to return f0
%
% Example: 
%
% Other m-files required: none
% Subfunctions: none
% MAT-files required: none
%
% See also: 

% Author:       Matthias Althoff
% Written:      17-January-2008
% Last update:  29-June-2009
%               23-July-2009
%               16-August-2016
% Last revision: ---

%------------- BEGIN CODE --------------

%extract set and error
Rinit = Rstart.set;
error = Rstart.error;

% linearize nonlinear system
[obj,linSys,linOptions] = linearize(obj,options,Rinit); 

%translate Rinit by linearization point
Rdelta=Rinit+(-obj.linError.p.x);

% compute reachable set of linearized system
%ti: time interval, tp: time point
[linSys,R] = initReach_inputDependence(linSys,Rdelta,linOptions);
%[linSys2,R2] = initReach(linSys,Rdelta,linOptions);
Rtp=R.tp;
Rti=R.ti;

perfIndCurr=inf;
perfInd=0;
while (perfIndCurr>1) && (perfInd<=1) 
    
    %new technique: compute reachable set due to assumed linearization error
    appliedError = 1.1*error;
    Verror = zonotope([0*appliedError,diag(appliedError)]);
    [RallError] = errorSolution(linSys,Verror,options);     

    % obtain linearization error
    if options.advancedLinErrorComp
        
        %compute maximum reachable set due to maximal allowed linearization error
        Rmax=Rti+RallError;
        [Verror,trueError] = linError_quadratic(obj,options,Rmax);

        %NOT YET IMPLEMENTED:
%         if options.tensorOrder<=2
%             %compute maximum reachable set due to maximal allowed linearization error
%             %Rmax=Rti+RallError;
%             try
%                 Rmax=Rtp+zonotope(Rdiff)+RallError;
%             catch
%                 Rmax=Rtp+Rdiff+RallError; 
%             end
%             
%             [VerrorDyn,trueError] = linError_mixed_noInt(obj,options,Rmax); 
%             VerrorStat = [];
%         else
%             %compute maximum reachable set due to maximal allowed linearization error
%             try
%                 Rmax=Rtp+zonotope(Rdiff)+RallError;
%             catch
%                 Rmax=Rtp+Rdiff+RallError; 
%             end
%             
%             [VerrorStat,VerrorDyn,trueError] = linError_thirdOrder(obj,options,Rmax,Rdiff);
%         end
    else
        %compute maximum reachable set due to maximal allowed linearization error
        Rmax=Rti+RallError;         
        
        [trueError] = linError(obj,options,Rmax);
        VerrorDyn=zonotope([0*trueError,diag(trueError)]);
        VerrorStat = [];
    end

    %store old error
    error = trueError;

    %compute performance index of linearization error
    perfIndCurr = max(trueError./appliedError);    
    perfInd = max(trueError./obj.allowedError);
    
end
% compute reachable set due to the linearization error
if ~isempty(VerrorStat)
    [Rerror] = errorSolutionQuad(linSys,VerrorStat,VerrorDyn,options); 
else
    [Rerror] = errorSolution(linSys,VerrorDyn,options); 
end

%translate reachable sets by linearization point
Rti=Rti+obj.linError.p.x;
Rtp=Rtp+obj.linError.p.x;

if (perfInd>1)  && recur
    %find best split
    nr=select(obj,options,Rstart);
elseif recur==0
    %return performance index instead of number if function is called
    %from select() using recur=0
    nr=perfInd;
else
    nr=[];
end

%add intervalhull of actual error
if isa(Rerror,'quadZonotope')
    Rti=exactPlus(Rti,Rerror);
    Rtp=exactPlus(Rtp,Rerror);
else
    Rti=Rti+Rerror;
    Rtp=Rtp+Rerror;
end

%add error to set
RtpEnh.set=Rtp;
RtpEnh.error=error;

%------------- END OF CODE --------------