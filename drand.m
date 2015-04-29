function X = drand(p,m,n)

% Use the Matlab editor to open a file.  Cut and paste this pdf into the
% editor and save it as 'drand.m' .  Then, from the command window, you can
% run drand.m using, for example,
%
% >> p=[.1 .2 .6 .05 .05];
% >> X=drand(p,20,2);
%
% In general, p is an S-length nonnegative vector that sums to 1.
%
% X is an m x n matrix of iid random observations
% taking values in 1,2,...,S with P(X(i,j)=k) = p(k).
%

% This function can take 1, 2, or 3 arguments ( drand(p), drand(p,m), or
% drand(p,m,n) ).

if nargin < 3, n = 1; end
if nargin < 2, m = 1; end

% get the size of the state space for X: 1,2,...,S

S = length(p);

% initialize X

X = zeros(m,n);

% loop over columns in X

for j = 1:n

    % loop over rows in X
    
    for i = 1:m
    
        % Determine X(i,j)
        
        % get a U(0,1) rv
        
        U = rand;
        
        %---- find out where it lands in the cdf of X ----%
        
        % initialize the cdf
        
        F = 0;
        
        % loop over possible values for X
        
        for k = 1:S
            
            % update the cdf
            
            F = F + p(k);
            
            % if U lands in this piece of the cdf, then set X(i,j)=k and 
            % stop
            
            if U <= F
                
                X(i,j) = k;
                break
            
            end
            
        end 
        
    end % loop over i
    
end % loop over j
