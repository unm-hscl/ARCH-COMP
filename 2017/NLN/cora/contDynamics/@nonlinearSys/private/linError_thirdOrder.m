function [errorStat, errorDyn, errorInt] = linError_thirdOrder(obj, options, R, Rdiff)
% linError - computes the linearization error
%
% Syntax:  
%    [obj] = linError(obj,options)
%
% Inputs:
%    obj - nonlinear DAE system object
%    options - options struct
%    R - actual reachable set
%
% Outputs:
%    error - zonotope overapproximating the linearization error
%    errorInt - interval overapproximating the linearization error
%
% Example: 
%
% Other m-files required: none
% Subfunctions: none
% MAT-files required: none
%
% See also: 

% Author:       Matthias Althoff
% Written:      21-August-2012
% Last update:  18-March-2016
%               25-July-2016 (intervalhull replaced by interval)
% Last revision:---

%------------- BEGIN CODE --------------

%compute interval of reachable set
dx = interval(R);
totalInt_x = dx + obj.linError.p.x;

%compute intervals of input
du = interval(options.U);
totalInt_u = du + obj.linError.p.u;

%compute zonotope of state and input
Rred = reduce(R,options.reductionTechnique,options.errorOrder);
if isa(R,'zonotope')
    Rred_zono = reduce(R,options.reductionTechnique,options.errorOrder);
    Rred_diff = reduce(Rdiff,options.reductionTechnique,options.errorOrder);    
else
    Rred_zono = reduce(zonotope(R),options.reductionTechnique,options.errorOrder);
    Rred_diff = reduce(zonotope(Rdiff),options.reductionTechnique,options.errorOrder);
end
Z=cartesianProduct(Rred,options.U);
Z_zono=cartesianProduct(Rred_zono,options.U);
Z_diff=cartesianProduct(Rred_diff,options.U);

%obtain intervals and combined interval z
dz = [dx; du];

%obtain absolute values
dz_abs = max(abs(infimum(dz)), abs(supremum(dz)));

%obtain hessian tensor and third order tensor
H = obj.hessian(obj.linError.p.x, obj.linError.p.u);

% if ~isempty(options.preT)
%     %find index
%     index = round(obj.linError.p.x(end)/options.preT{1}.stepSize_1);
%     
%     %check correctness
%     %if (IH_x + obj.linError.p.x) <= options.preT{index}.IH
%         T = options.preT{index}.T;
%     %end
% else

% tic
T = obj.thirdOrderTensor(totalInt_x, totalInt_u);
%T = thirdOrderTensor_reduced(totalInt_x, totalInt_u);
% toc
%tic
%T = thirdOrderTensor_reduced2_parallel(totalInt_x, totalInt_u);
%toc


%dynamic error
error_secondOrder_dyn = 0.5*(mixedMultiplication(Z_zono,Z_diff,H) ...
              + mixedMultiplication(Z_diff,Z_zono,H) ...
              + quadraticMultiplication(Z_diff,H));

%second order error
error_secondOrder_stat = 0.5*quadraticMultiplication(Z, H);

%ACTIVATE FOR agingSys!!!!!
%interval evaluation
for i=1:length(T(:,1))
    error_sum = interval(0,0);
    for j=1:length(T(1,:))
        error_tmp(i,j) = dz.'*T{i,j}*dz;
        error_sum = error_sum + error_tmp(i,j) * dz(j);
    end
    error_thirdOrder_old(i,1) = 1/6*error_sum;
end

error_thirdOrder_dyn = zonotope(error_thirdOrder_old);

% %ACTIVATE FOR vanDerPOL!!!!!
% %interval evaluation 
% for i=1:length(T(:,1))
%     error_sum = 0;
%     for j=1:length(T(1,:))
%         T_abs = sup(abs(T{i,j}));
%         error_tmp(i,j) = dz_abs'*T_abs*dz_abs;
%         error_sum = error_sum + error_tmp(i,j) * dz_abs(j);
%     end
%     error_thirdOrder_abs(i,1) = 1/6*error_sum;
% end
% 
% error_thirdOrder_dyn = zonotope(interval(-error_thirdOrder_abs,error_thirdOrder_abs));

% %alternative
% %separate evaluation
% for i=1:length(T(:,1))
%     for j=1:length(T(1,:))
%         T_mid{i,j} = sparse(mid(T{i,j}));
%         T_rad{i,j} = sparse(rad(T{i,j}));
%     end
% end
% 
% 
% error_mid = 1/6*cubicMultiplication(Z_zono, T_mid);
% 
% %interval evaluation
% for i=1:length(T(:,1))
%     error_sum2 = 0;
%     for j=1:length(T(1,:))
%         error_tmp2(i,j) = dz_abs'*T_rad{i,j}*dz_abs;
%         error_sum2 = error_sum2 + error_tmp2(i,j) * dz_abs(j);
%     end
%     error_rad(i,1) = 1/6*error_sum2;
% end
% 
% 
% %combine results
% error_rad_zono = zonotope(interval(-error_rad, error_rad));
% error_thirdOrder_dyn = error_mid + error_rad_zono;

error_thirdOrder_dyn = reduce(error_thirdOrder_dyn,'girard',options.zonotopeOrder);

%combine results
errorDyn = error_secondOrder_dyn + error_thirdOrder_dyn;
errorStat= error_secondOrder_stat;

errorDyn = reduce(errorDyn,'girard',options.intermediateOrder);
errorStat = reduce(errorStat,'girard',options.intermediateOrder);

errorIHabs = abs(interval(errorDyn) + interval(errorStat));
errorInt = supremum(errorIHabs);

%------------- END OF CODE --------------