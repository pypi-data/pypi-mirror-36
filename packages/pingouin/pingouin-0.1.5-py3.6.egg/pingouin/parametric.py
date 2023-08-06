# Author: Raphael Vallat <raphaelvallat9@gmail.com>
# Date: April 2018
import numpy as np
import pandas as pd
from pingouin import (_check_dataframe, _remove_rm_na, _remove_na,
                      _export_table, bayesfactor_ttest)

__all__ = ["gzscore", "test_normality", "test_homoscedasticity", "test_dist",
           "epsilon", "test_sphericity", "ttest", "rm_anova", "anova",
           "anova2", "mixed_anova"]


def gzscore(x):
    """Geometric standard (Z) score.

    Geometric Z-scores are better measures of dispersion than arithmetic
    z-scores when the sample data come from a log-normally distributed
    population.

    See https://en.wikipedia.org/wiki/Geometric_standard_deviation

    Parameters
    ----------
    x : array_like
        Array of raw values

    Returns
    -------
    gzscore : array_like
        Array of geometric z-scores (same shape as x)

    Examples
    --------
    Standardize a log-normal array

        >>> import numpy as np
        >>> from pingouin import gzscore
        >>> np.random.seed(123)
        >>> raw = np.random.lognormal(size=100)
        >>> print(raw.mean().round(3), raw.std().round(3))
            1.849 2.282
        >>> z = gzscore(raw)
        >>> print(z.mean(), z.std())
            0 0.995
    """
    from scipy.stats import gmean
    # Geometric mean
    geo_mean = gmean(x)
    # Geometric standard deviation
    gstd = np.exp(np.sqrt(np.sum((np.log(x / geo_mean))**2) / (len(x) - 1)))
    # Geometric z-score
    return np.log(x / geo_mean) / np.log(gstd)


def test_normality(*args, alpha=.05):
    """Test the normality of one or more array.

    Parameters
    ----------
    sample1, sample2,... : array_like
        Array of sample data. May be different lengths.

    Returns
    -------
    normal : boolean
        True if x comes from a normal distribution.
    p : float
        P-value.

    See Also
    --------
    test_homoscedasticity : Test equality of variance.
    test_sphericity : Mauchly's test for sphericity.

    Examples
    --------
    1. Test the normality of one array.

        >>> import numpy as np
        >>> from pingouin import test_normality
        >>> np.random.seed(123)
        >>> x = np.random.normal(size=100)
        >>> normal, p = test_normality(x, alpha=.05)
        >>> print(normal, p)
        True 0.27

    2. Test the normality of two arrays.

        >>> import numpy as np
        >>> from pingouin import test_normality
        >>> np.random.seed(123)
        >>> x = np.random.normal(size=100)
        >>> y = np.random.rand(100)
        >>> normal, p = test_normality(x, y, alpha=.05)
        >>> print(normal, p)
        [True   False] [0.27   0.0005]
    """
    from scipy.stats import shapiro
    k = len(args)
    p = np.zeros(k)
    normal = np.zeros(k, 'bool')
    for j in range(k):
        _, p[j] = shapiro(args[j])
        normal[j] = True if p[j] > alpha else False

    if k == 1:
        normal = bool(normal)
        p = float(p)

    return normal, np.round(p, 3)


def test_homoscedasticity(*args, alpha=.05):
    """Test equality of variance.

    If data are normally distributed, uses Bartlett (1937).
    If data are not-normally distributed, uses Levene (1960).

    Parameters
    ----------
    sample1, sample2,... : array_like
        Array of sample data. May be different lengths.

    Returns
    -------
    equal_var : boolean
        True if data have equal variance.
    p : float
        P-value.

    See Also
    --------
    test_normality : Test the normality of one or more array.
    test_sphericity : Mauchly's test for sphericity.

    Examples
    --------
    Test the homoscedasticity of two arrays.

        >>> import numpy as np
        >>> from pingouin import test_homoscedasticity
        >>> np.random.seed(123)
        >>> # Scale = standard deviation of the distribution.
        >>> x = np.random.normal(loc=0, scale=1., size=100)
        >>> y = np.random.normal(loc=0, scale=0.8,size=100)
        >>> print(np.var(x), np.var(y))
            1.27 0.60
        >>> equal_var, p = test_homoscedasticity(x, y, alpha=.05)
        >>> print(equal_var, p)
            False 0.0002
    """
    from scipy.stats import levene, bartlett
    k = len(args)
    if k < 2:
        raise ValueError("Must enter at least two input sample vectors.")

    # Test normality of data
    normal, _ = test_normality(*args)
    if np.count_nonzero(normal) != normal.size:
        # print('Data are not normally distributed. Using Levene test.')
        _, p = levene(*args)
    else:
        _, p = bartlett(*args)

    equal_var = True if p > alpha else False
    return equal_var, np.round(p, 3)


def test_dist(*args, dist='norm'):
    """Anderson-Darling test of distribution.

    Parameters
    ----------
    sample1, sample2,... : array_like
        Array of sample data. May be different lengths.
    dist : string
        Distribution ('norm', 'expon', 'logistic', 'gumbel')

    Returns
    -------
    from_dist : boolean
        True if data comes from this distribution.
    """
    from scipy.stats import anderson
    k = len(args)
    from_dist = np.zeros(k, 'bool')
    sig_level = np.zeros(k)
    for j in range(k):
        st, cr, sig = anderson(args[j], dist=dist)
        from_dist[j] = True if (st > cr).any() else False
        sig_level[j] = sig[np.argmin(np.abs(st - cr))]

    if k == 1:
        from_dist = bool(from_dist)
        sig_level = float(sig_level)
    return from_dist, sig_level


def epsilon(data, correction='gg'):
    """Compute Epsilon adjustement factor for repeated measurements.

    Parameters
    ----------
    data : pd.DataFrame
        DataFrame containing the repeated measurements.

        Note that data are NOT expected to be in long format but rather with
        shape (n_subj, n_groups). If your data are in long format, use the
        pandas pivot function first.
    correction : string
        Specify the epsilon version ::

            'gg' : Greenhouse-Geisser
            'hf' : Huynh-Feldt

    Returns
    -------
    eps : float
        Epsilon adjustement factor.
    """
    # Covariance matrix
    S = data.cov()
    n = data.shape[0]
    k = data.shape[1]
    mean_var = np.diag(S).mean()
    S_mean = S.mean().mean()
    ss_mat = (S**2).sum().sum()
    ss_rows = (S.mean(1)**2).sum().sum()

    # Compute GGEpsilon
    num = (k * (mean_var - S_mean))**2
    den = (k - 1) * (ss_mat - 2 * k * ss_rows + k**2 * S_mean**2)
    eps = num / den

    if correction == 'hf':
        num = n * (k - 1) * eps - 2
        den = (k - 1) * (n - 1 - (k - 1) * eps)
        eps = np.min([num / den, 1])

    return eps


def test_sphericity(data, alpha=.05):
    """Mauchly's test for sphericity

    Parameters
    ----------
    data : pd.DataFrame
        DataFrame containing the repeated measurements.

        Note that data are NOT expected to be in long format but rather with
        shape (n_subj, n_groups). If your data are in long format, use the
        pandas pivot function first.
    alpha : float, optional
        Significance level

    Returns
    -------
    sphericity : boolean
        True if data have the sphericity property.
    W : float
        Test statistic
    chi_sq : float
        Chi-square statistic
    ddof : int
        Degrees of freedom
    p : float
        P-value.

    See Also
    --------
    test_homoscedasticity : Test equality of variance.
    test_normality : Test the normality of one or more array.
    """
    from scipy.stats import chi2
    S = data.cov()
    n = data.shape[0]
    p = data.shape[1]
    d = p - 1

    # if method == 'jsn':
    #     eps = epsilon(data, correction='gg')
    #     W = eps * d
    #     chi_sq = 0.5 * n * d ** 2 * (W - 1 / d)

    # Population covariance
    S_mean = S.mean().mean()
    S_pop = pd.DataFrame()
    S['mean'] = S.mean(1)
    S.loc['mean', :] = S.mean(0)

    for k in S.keys().drop('mean'):
        for l in S.index.drop('mean'):
            S_pop.loc[k, l] = S.loc[k, l] - S.loc[k, 'mean'] - \
                S.loc['mean', l] + S_mean

    # Eigenvalues
    eig = np.linalg.eigvals(S_pop)
    # Remove very low eigenvalues
    eig = eig[eig > 1e-4]

    # Mauchly's statistic
    W = np.product(eig) / (eig.sum() / d)**d

    # Chi-square
    f = (2 * d**2 + p + 1) / (6 * d * (n - 1))
    chi_sq = (f - 1) * (n - 1) * np.log(W)

    # Compute dof and pval
    ddof = d * p / 2 - 1
    pval = chi2.sf(chi_sq, ddof)

    # Second order approximation
    # pval2 = chi2.sf(chi_sq, ddof + 4)
    # w2 = (d + 2) * (d - 1) * (d - 2) * (2 * d**3 + 6 * d * d + 3 * d + 2) / \
    #      (288 * d * d * nr * nr * dd * dd)
    # pval += w2 * (pval2 - pval)

    sphericity = True if pval > alpha else False
    return sphericity, W, chi_sq, ddof, pval


def ttest(x, y, paired=False, tail='two-sided', correction='auto', r=.707):
    """T-test.

    Parameters
    ----------
    x : array_like
        First set of observations.
    y : array_like or float
        Second set of observations. If y is a single value, a one-sample T-test
        is computed.
    paired : boolean
        Specify whether the two observations are related (i.e. repeated
        measures) or independant.
    tail : string
        Specify whether to return two-sided or one-sided p-value.
    correction : string or boolean
        For unpaired two sample T-tests, specify whether or not to correct for
        unequal variances using Welch separate variances T-test. If 'auto', it
        will automatically uses Welch T-test when the sample sizes are unequal,
        as recommended by Zimmerman 2004.
    r : float
        Cauchy scale factor for computing the Bayes Factor.
        Smaller values of r (e.g. 0.5), may be appropriate when small effect
        sizes are expected a priori; larger values of r are appropriate when
        large effect sizes are expected (Rouder et al 2009).
        The default is 0.707 (= np.sqrt(2) / 2).

    Returns
    -------
    stats : pandas DataFrame
        T-test summary ::

        'T-val' : T-value
        'p-val' : p-value
        'dof' : degrees of freedom
        'cohen-d' : Cohen d effect size
        'power' : achieved power of the test ( = 1 - type II error)
        'BF10' : Bayes Factor of the alternative hypothesis

    Notes
    -----
    Missing values are automatically removed from the data. If x and y are
    paired, the entire row is removed.

    Examples
    --------
    1. One-sample T-test.

        >>> from pingouin import ttest
        >>> x = [5.5, 2.4, 6.8, 9.6, 4.2]
        >>> ttest(x, 4)
            T-val   p-val  dof  cohen-d  power   BF10
            1.397  0.2348    4    0.699  0.226  0.766

    2. Paired two-sample T-test (one-tailed).

        >>> from pingouin import ttest
        >>> pre = [5.5, 2.4, 6.8, 9.6, 4.2]
        >>> post = [6.4, 3.4, 6.4, 11., 4.8]
        >>> ttest(pre, post, paired=True, tail='one-sided')
            T-val   p-val  dof  cohen-d  power   BF10
            -2.308   0.04    4     0.28  0.132  1.864

    3. Paired two-sample T-test with missing values.

        >>> from pingouin import ttest
        >>> from numpy import nan
        >>> pre = [5.5, 2.4, nan, 9.6, 4.2]
        >>> post = [6.4, 3.4, 6.4, 11., 4.8]
        >>> ttest(pre, post, paired=True)
            T-val    p-val  dof  cohen-d  power    BF10
            -5.902  0.0097    3   -0.354  0.074  24.926

    4. Independant two-sample T-test (equal sample size).

        >>> from pingouin import ttest
        >>> import numpy as np
        >>> np.random.seed(123)
        >>> x = np.random.normal(loc=7, size=20)
        >>> y = np.random.normal(loc=4, size=20)
        >>> ttest(x, y, correction='auto')
            T-val     p-val  dof  cohen-d  power   BF10
            9.106  4.30e-11   38     2.88    1.0  1.4e8

    5. Independant two-sample T-test (unequal sample size).

        >>> from pingouin import ttest
        >>> import numpy as np
        >>> np.random.seed(123)
        >>> x = np.random.normal(loc=7, size=20)
        >>> y = np.random.normal(loc=6.5, size=15)
        >>> ttest(x, y, correction='auto')
            T-val     p-val  dof   dof-corr  cohen-d  power   BF10
            2.327     0.027   33      30.75    0.792  0.614  2.454
    """
    from scipy.stats import ttest_rel, ttest_ind, ttest_1samp
    from pingouin import ttest_power, compute_effsize
    x = np.asarray(x)
    y = np.asarray(y)

    if x.size != y.size and paired:
        print('x and y have unequal sizes. Switching to paired == False.')
        paired = False

    # Remove NA
    x, y = _remove_na(x, y, paired=paired)
    nx = x.size
    ny = y.size
    stats = pd.DataFrame({}, index=['T-test'])

    if ny == 1:
        # Case one sample T-test
        tval, pval = ttest_1samp(x, y)
        dof = nx - 1
        pval = pval / 2 if tail == 'one-sided' else pval

    if ny > 1 and paired is True:
        # Case paired two samples T-test
        tval, pval = ttest_rel(x, y)
        dof = nx - 1
        bf = bayesfactor_ttest(tval, nx, ny, paired=True, r=r)

    elif ny > 1 and paired is False:
        dof = nx + ny - 2
        # Case unpaired two samples T-test
        if correction is True or (correction == 'auto' and nx != ny):
            # Use the Welch separate variance T-test
            tval, pval = ttest_ind(x, y, equal_var=False)
            # dof are approximated using Welch–Satterthwaite equation
            vx = x.var(ddof=1)
            vy = y.var(ddof=1)
            dof_corr = (vx / nx + vy / ny)**2 / ((vx / nx)**2 / (nx - 1) +
                                                 (vy / ny)**2 / (ny - 1))
            stats['dof-corr'] = dof_corr
        else:
            tval, pval = ttest_ind(x, y, equal_var=True)

    pval = pval / 2 if tail == 'one-sided' else pval

    # Effect size and achieved power
    d = compute_effsize(x, y, paired=paired, eftype='cohen')
    power = ttest_power(d, nx, ny, paired=paired, tail=tail)

    # Bayes factor
    bf = bayesfactor_ttest(tval, nx, ny, paired=paired, tail=tail, r=r)

    # Fill output DataFrame
    stats['dof'] = dof
    stats['T-val'] = tval.round(3)
    stats['p-val'] = pval
    stats['tail'] = tail
    stats['cohen-d'] = np.abs(d).round(3)
    stats['power'] = power
    stats['BF10'] = bf

    col_order = ['T-val', 'p-val', 'dof', 'dof-corr', 'tail', 'cohen-d',
                 'power', 'BF10']
    stats = stats.reindex(columns=col_order)
    stats.dropna(how='all', axis=1, inplace=True)
    return stats


def rm_anova(dv=None, within=None, subject=None, data=None, correction='auto',
             remove_na=True, detailed=False, export_filename=None):
    """One-way repeated measures ANOVA (type II).

    Results have been tested against R and JASP.

    Parameters
    ----------
    dv : string
        Name of column containing the dependant variable.
    within : string
        Name of column containing the within factor.
    subject : string
        Name of column containing the subject identifier.
    data : pandas DataFrame
        DataFrame
    correction : string or boolean
        If True, return Greenhouse-Geisser corrected p-value.
        If 'auto' (default), compute Mauchly's test of sphericity to determine
        whether the p-values needs to be corrected.
    remove_na : boolean
        If True, automatically remove from the analysis subjects with one or
        more missing values::

            Ss    x1       x2       x3
            1     5.0      4.2      nan
            2     4.6      3.6      3.9

        In this example, if remove_na == True, Ss 1 will be removed from the
        ANOVA because of the x3 missing value. If False, the two non-missing
        values will be included in the analysis.
    detailed : boolean
        If True, return a full ANOVA table
    export_filename : string
        Filename (without extension) for the output file.
        If None, do not export the table.
        By default, the file will be created in the current python console
        directory. To change that, specify the filename with full path.

    Returns
    -------
    aov : DataFrame
        ANOVA summary ::

        'Source' : Name of the within-group factor
        'ddof1' : Degrees of freedom (numerator)
        'ddof2' : Degrees of freedom (denominator)
        'F' : F-value
        'p-unc' : Uncorrected p-value
        'np2' : Partial eta-square effect size
        'eps' : Greenhouse-Geisser epsilon factor (= index of sphericity)
        'p-GG-corr' : Greenhouse-Geisser corrected p-value
        'W-Mauchly' : Mauchly statistic
        'p-Mauchly' : p-value of the Mauchly test
        'sphericity' : sphericity of the data (boolean)

    See Also
    --------
    anova : One-way ANOVA
    mixed_anova : Two way mixed ANOVA
    friedman : Non-parametric one-way repeated measures ANOVA

    Notes
    -----
    Data are expected to be in long-format.

    Note that if the dataset contains one or more other within subject
    factors, an automatic collapsing to the mean is applied on the dependant
    variable (same behavior as the ezANOVA R package). As such, results can
    differ from those of JASP. If you can, always double-check the results.

    The effect size reported in Pingouin is the partial eta-square.
    However, one should keep in mind that for one-way repeated-measures ANOVA,
    partial eta-square is the same as eta-square
    (Bakeman 2005; Richardson 2011).

    Examples
    --------
    Compute a one-way repeated-measures ANOVA.

        >>> import pandas as pd
        >>> from pingouin import rm_anova, print_table
        >>> df = pd.read_csv('dataset.csv')
        >>> aov = rm_anova(dv='DV', within='Time', subject='Subject',
                           data=df, correction='auto', remove_na=True,
                           detailed=True, export_filename='rm_anova.csv')
        >>> print_table(aov)
    """
    from scipy.stats import f

    # Check data
    _check_dataframe(dv=dv, within=within, data=data, subject=subject,
                     effects='within')

    # Collapse to the mean
    data = data.groupby([subject, within]).mean().reset_index()

    # Remove NaN
    if remove_na and data[dv].isnull().any():
        data = _remove_rm_na(dv=dv, within=within, subject=subject, data=data)

    # Groupby
    grp_with = data.groupby(within)[dv]
    rm = list(data[within].unique())
    n_rm = len(rm)
    n_obs = int(data.groupby(within)[dv].count().max())
    grandmean = data[dv].mean()

    # Calculate sums of squares
    sstime = ((grp_with.mean() - grandmean)**2 * grp_with.count()).sum()
    sswithin = grp_with.apply(lambda x: (x - x.mean())**2).sum()
    grp_subj = data.groupby(subject)[dv]
    sssubj = n_rm * np.sum((grp_subj.mean() - grandmean)**2)
    sserror = sswithin - sssubj

    # Calculate degrees of freedom
    ddof1 = n_rm - 1
    ddof2 = ddof1 * (n_obs - 1)

    # Calculate F and p-values
    mserror = sserror / (ddof2 / ddof1)
    fval = sstime / mserror
    p_unc = f(ddof1, ddof2).sf(fval)

    # Calculating partial eta-square
    # Similar to (fval * ddof1) / (fval * ddof1 + ddof2)
    np2 = sstime / (sstime + sserror)

    # Reshape and remove NAN for sphericity estimation and correction
    data_pivot = data.pivot(index=subject, columns=within, values=dv).dropna()

    # Compute sphericity using Mauchly's test
    # Sphericity assumption only applies if there are more than 2 levels
    if correction == 'auto' or (correction is True and n_rm >= 3):
        sphericity, W_mauchly, chi_sq_mauchly, ddof_mauchly, \
            p_mauchly = test_sphericity(data_pivot, alpha=.05)
        if correction == 'auto':
            correction = True if not sphericity else False
    else:
        correction = False

    # Compute epsilon adjustement factor
    eps = epsilon(data_pivot, correction='gg')

    # If required, apply Greenhouse-Geisser correction for sphericity
    if correction:
        corr_ddof1, corr_ddof2 = [np.maximum(d * eps, 1.) for d in
                                  (ddof1, ddof2)]
        p_corr = f(corr_ddof1, corr_ddof2).sf(fval)

    # Create output dataframe
    if not detailed:
        aov = pd.DataFrame({'Source': within,
                            'ddof1': ddof1,
                            'ddof2': ddof2,
                            'F': fval,
                            'p-unc': p_unc,
                            'np2': np2,
                            'eps': eps,
                            }, index=[0])
        if correction:
            aov['p-GG-corr'] = p_corr
            aov['W-Mauchly'] = W_mauchly
            aov['p-Mauchly'] = p_mauchly
            aov['sphericity'] = sphericity

        col_order = ['Source', 'ddof1', 'ddof2', 'F', 'p-unc',
                     'p-GG-corr', 'np2', 'eps', 'sphericity', 'W-Mauchly',
                     'p-Mauchly']
    else:
        aov = pd.DataFrame({'Source': [within, 'Error'],
                            'SS': np.round([sstime, sserror], 3),
                            'DF': [ddof1, ddof2],
                            'MS': np.round([sstime / ddof1, sserror / ddof2],
                                           3),
                            'F': [fval, np.nan],
                            'p-unc': [p_unc, np.nan],
                            'np2': [np2, np.nan],
                            'eps': [eps, np.nan]
                            })
        if correction:
            aov['p-GG-corr'] = [p_corr, np.nan]
            aov['W-Mauchly'] = [W_mauchly, np.nan]
            aov['p-Mauchly'] = [p_mauchly, np.nan]
            aov['sphericity'] = [sphericity, np.nan]

        col_order = ['Source', 'SS', 'DF', 'MS', 'F', 'p-unc', 'p-GG-corr',
                     'np2', 'eps', 'sphericity', 'W-Mauchly', 'p-Mauchly']

    # Round
    aov[['F', 'eps', 'np2']] = aov[['F', 'eps', 'np2']].round(3)

    # Replace NaN
    aov = aov.fillna('-')

    aov = aov.reindex(columns=col_order)
    aov.dropna(how='all', axis=1, inplace=True)
    # Export to .csv
    if export_filename is not None:
        _export_table(aov, export_filename)
    return aov


def anova(dv=None, between=None, data=None, detailed=False,
          export_filename=None):
    """One-way and two-way ANOVA.

    Results have been tested against R, Matlab and JASP.

    Parameters
    ----------
    dv : string
        Name of column containing the dependant variable.
    between : string or list
        Name(s) of column containing the between factor.
        If between is a single string, then compute a one-way ANOVA, if between
        is a list with two strings, compute a two-way ANOVA.
    data : pandas DataFrame
        DataFrame
    detailed : boolean
        If True, return a detailed ANOVA table
    export_filename : string
        Filename (without extension) for the output file.
        If None, do not export the table.
        By default, the file will be created in the current python console
        directory. To change that, specify the filename with full path.

    Returns
    -------
    aov : DataFrame
        ANOVA summary ::

        'Source' : Factor names
        'SS' :Sums of squares
        'DF' : Degrees of freedom
        'MS' : Mean squares
        'F' : F-values
        'p-unc' : uncorrected p-values
        'np2' : Partial eta-square effect sizes

    See Also
    --------
    rm_anova : One-way repeated measures ANOVA
    mixed_anova : Two way mixed ANOVA
    kruskal : Non-parametric one-way ANOVA


    Notes
    -----
    The effect size reported in Pingouin is the partial eta-square.
    However, one should keep in mind that for one-way ANOVA
    partial eta-square is the same as eta-square and generalized eta-square.

    For more details, see Bakeman 2005; Richardson 2011.

    Examples
    --------
    1. One-way ANOVA on the pain threshold dataset.

        >>> from pingouin import anova, print_table
        >>> from pingouin.dataset import read_dataset
        >>> df = read_dataset('mcclave1991')
        >>> aov = anova(dv='Pain threshold', between='Hair color', data=df,
                        detailed=True, export_filename='pain_anova.csv')
        >>> print_table(aov)

    2. Two-way ANOVA.

        >>> import pandas as pd
        >>> from pingouin import anova, print_table
        >>> df = pd.read_csv('dataset.csv')
        >>> aov = anova(dv='DV', between=['factor1, 'factor2'], data=df,
                        export_filename='anova.csv')
        >>> print_table(aov)

    """
    if isinstance(between, list):
        if len(between) == 2:
            return anova2(dv=dv, between=between, data=data,
                          export_filename=export_filename)
        elif len(between) == 1:
            between = between[0]

    # Check data
    _check_dataframe(dv=dv, between=between, data=data, effects='between')

    # Reset index (avoid duplicate axis error)
    data = data.reset_index(drop=True)

    groups = list(data[between].unique())
    n_groups = len(groups)
    N = data[dv].size

    # Calculate sums of squares
    grp = data.groupby(between)[dv]
    # Between effect
    ssbetween = ((grp.mean() - data[dv].mean())**2 * grp.count()).sum()
    # Within effect (= error between)
    sserror = grp.apply(lambda x: (x - x.mean())**2).sum()

    # Calculate DOF, MS, F and p-values
    ddof1 = n_groups - 1
    ddof2 = N - n_groups
    msbetween = ssbetween / ddof1
    mserror = sserror / ddof2
    fval = msbetween / mserror
    from scipy.stats import f
    p_unc = f(ddof1, ddof2).sf(fval)

    # Calculating partial eta-square
    # Similar to (fval * ddof1) / (fval * ddof1 + ddof2)
    np2 = ssbetween / (ssbetween + sserror)

    # Create output dataframe
    if not detailed:
        aov = pd.DataFrame({'Source': between,
                            'ddof1': ddof1,
                            'ddof2': ddof2,
                            'F': fval,
                            'p-unc': p_unc,
                            'np2': np2
                            }, index=[0])

        col_order = ['Source', 'ddof1', 'ddof2', 'F', 'p-unc', 'np2']
    else:
        aov = pd.DataFrame({'Source': [between, 'Within'],
                            'SS': np.round([ssbetween, sserror], 3),
                            'DF': [ddof1, ddof2],
                            'MS': np.round([msbetween, mserror], 3),
                            'F': [fval, np.nan],
                            'p-unc': [p_unc, np.nan],
                            'np2': [np2, np.nan]
                            })
        col_order = ['Source', 'SS', 'DF', 'MS', 'F', 'p-unc', 'np2']

    # Round
    aov[['F', 'np2']] = aov[['F', 'np2']].round(3)

    # Replace NaN
    aov = aov.fillna('-')

    aov = aov.reindex(columns=col_order)
    aov.dropna(how='all', axis=1, inplace=True)
    # Export to .csv
    if export_filename is not None:
        _export_table(aov, export_filename)
    return aov


def anova2(dv=None, between=None, data=None, export_filename=None):
    """Two-way ANOVA.

    Results have been tested against JASP.

    Parameters
    ----------
    dv : string
        Name of column containing the dependant variable.
    between : list of string
        Name of column containing the two between factors. Must contain exactly
        two values (e.g. ['factor1', 'factor2'])
    data : pandas DataFrame
        DataFrame
    export_filename : string
        Filename (without extension) for the output file.
        If None, do not export the table.
        By default, the file will be created in the current python console
        directory. To change that, specify the filename with full path.

    Returns
    -------
    aov : DataFrame
        ANOVA summary ::

        'Source' : Factor names
        'SS' :Sums of squares
        'DF' : Degrees of freedom
        'MS' : Mean squares
        'F' : F-values
        'p-unc' : uncorrected p-values
        'np2' : Partial eta-square effect sizes

    See Also
    --------
    anova : One-way ANOVA
    rm_anova : One-way repeated measures ANOVA
    mixed_anova : Two way mixed ANOVA
    kruskal : Non-parametric one-way ANOVA

    Examples
    --------
    Compute a two-way ANOVA.

        >>> import pandas as pd
        >>> from pingouin import anova2, print_table
        >>> df = pd.read_csv('dataset.csv')
        >>> aov = anova(dv='DV', between=['factor1', 'factor2'], data=df,
                        export_filename='anova.csv')
        >>> print_table(aov)
    """
    from scipy.stats import f

    # Assert that there are two factors
    if not isinstance(between, list):
        return anova(dv=dv, between=between, data=data,
                     export_filename=export_filename, detailed=True)

    if len(between) == 1:
        return anova(dv=dv, between=between[0], data=data,
                     export_filename=export_filename, detailed=True)

    # Reset index (avoid duplicate axis error)
    data = data.reset_index(drop=True)

    fac1, fac2 = between
    aov_fac1 = anova(data=data, dv=dv, between=fac1, detailed=True)
    aov_fac2 = anova(data=data, dv=dv, between=fac2, detailed=True)

    # Sums of squares
    ss_fac1 = aov_fac1.loc[0, 'SS']
    ss_fac2 = aov_fac2.loc[0, 'SS']
    ss_tot = ((data[dv] - data[dv].mean())**2).sum()
    ss_resid = np.sum(data.groupby([fac1, fac2]).apply(lambda x:
                                                       (x - x.mean())**2))[0]
    ss_inter = ss_tot - (ss_resid + ss_fac1 + ss_fac2)

    # Degrees of freedom
    df_fac1 = aov_fac1.loc[0, 'DF']
    df_fac2 = aov_fac2.loc[0, 'DF']
    df_inter = (data[fac1].unique().size - 1) * (data[fac2].unique().size - 1)
    df_resid = data[dv].size - (data[fac1].unique().size *
                                data[fac2].unique().size)

    # Mean squares
    ms_fac1 = aov_fac1.loc[0, 'MS']
    ms_fac2 = aov_fac2.loc[0, 'MS']
    ms_inter = ss_inter / df_inter
    ms_resid = ss_resid / df_resid

    # F-values
    fval_fac1 = ms_fac1 / ms_resid
    fval_fac2 = ms_fac2 / ms_resid
    fval_inter = ms_inter / ms_resid

    # P-values
    pval_fac1 = f(df_fac1, df_resid).sf(fval_fac1)
    pval_fac2 = f(df_fac2, df_resid).sf(fval_fac2)
    pval_inter = f(df_inter, df_resid).sf(fval_inter)

    # Partial eta-square
    np2_fac1 = (fval_fac1 * df_fac1) / (fval_fac1 * df_fac1 + df_resid)
    np2_fac2 = (fval_fac2 * df_fac2) / (fval_fac2 * df_fac2 + df_resid)
    np2_inter = (fval_inter * df_inter) / (fval_inter * df_inter + df_resid)

    # Create output dataframe
    aov = pd.DataFrame({'Source': [fac1, fac2, fac1 + ' * ' + fac2,
                                   'residual'],
                        'SS': np.round([ss_fac1, ss_fac2, ss_inter,
                                        ss_resid], 3),
                        'DF': [df_fac1, df_fac2, df_inter, df_resid],
                        'MS': np.round([ms_fac1, ms_fac2, ms_inter,
                                        ms_resid], 3),
                        'F': [fval_fac1, fval_fac2, fval_inter, np.nan],
                        'p-unc': [pval_fac1, pval_fac2, pval_inter, np.nan],
                        'np2': [np2_fac1, np2_fac2, np2_inter, np.nan]
                        })
    col_order = ['Source', 'SS', 'DF', 'MS', 'F', 'p-unc', 'np2']

    aov = aov.reindex(columns=col_order)
    aov.dropna(how='all', axis=1, inplace=True)
    # Export to .csv
    if export_filename is not None:
        _export_table(aov, export_filename)
    return aov


def mixed_anova(dv=None, within=None, subject=None, between=None, data=None,
                correction='auto', remove_na=True, export_filename=None):
    """Mixed-design (split-plot) type II ANOVA.

    Results have been tested against R and JASP.

    Parameters
    ----------
    dv : string
        Name of column containing the dependant variable.
    within : string
        Name of column containing the within factor.
    subject : string
        Name of column containing the subject identifier.
    between : string
        Name of column containing the between factor.
    data : pandas DataFrame
        DataFrame
    correction : string or boolean
        If True, return Greenhouse-Geisser corrected p-value.
        If 'auto' (default), compute Mauchly's test of sphericity to determine
        whether the p-values needs to be corrected.
    remove_na : boolean
        If True, automatically remove from the analysis subjects with one or
        more missing values::

            Ss    x1       x2       x3
            1     5.0      4.2      nan
            2     4.6      3.6      3.9

        In this example, if remove_na == True, Ss 1 will be removed from the
        ANOVA because of the x3 missing value. If False, the two non-missing
        values will be included in the analysis.
    export_filename : string
        Filename (without extension) for the output file.
        If None, do not export the table.
        By default, the file will be created in the current python console
        directory. To change that, specify the filename with full path.

    Returns
    -------
    aov : DataFrame
        ANOVA summary ::

        'Source' : Names of the factor considered
        'ddof1' : Degrees of freedom (numerator)
        'ddof2' : Degrees of freedom (denominator)
        'F' : F-values
        'p-unc' : Uncorrected p-values
        'np2' : Partial eta-square effect sizes
        'eps' : Greenhouse-Geisser epsilon factor ( = index of sphericity)
        'p-GG-corr' : Greenhouse-Geisser corrected p-values
        'W-Mauchly' : Mauchly statistic
        'p-Mauchly' : p-value of the Mauchly test
        'sphericity' : sphericity of the data (boolean)

    See Also
    --------
    anova : One-way ANOVA
    rm_anova : One-way repeated measures ANOVA

    Examples
    --------
    Compute a two-way mixed model ANOVA.

        >>> import pandas as pd
        >>> from pingouin import mixed_anova, print_table
        >>> df = pd.read_csv('dataset.csv')
        >>> aov = mixed_anova(dv='DV', within='Time', between='Group',
                              subject='Ss', data=df, correction='auto',
                              remove_na=False)
        >>> print_table(aov)
    """
    from scipy.stats import f

    # Check data
    _check_dataframe(dv=dv, within=within, between=between, data=data,
                     subject=subject, effects='interaction')

    # Collapse to the mean
    data = data.groupby([subject, within, between]).mean().reset_index()

    # Remove NaN
    if remove_na and data[dv].isnull().any():
        data = _remove_rm_na(dv=dv, within=within, subject=subject, data=data)

    # SUMS OF SQUARES
    grandmean = data[dv].mean()
    # Extract main effects of time and between
    mtime = rm_anova(dv=dv, within=within, subject=subject, data=data,
                     correction=correction, remove_na=False, detailed=True)
    mbetw = anova(dv=dv, between=between, data=data, detailed=True)
    # Extract SS total, residuals and interactions
    grp = data.groupby([between, within])[dv]
    sstotal = grp.apply(lambda x: (x - grandmean)**2).sum()
    # sst = residuals within + residuals between
    sst = grp.apply(lambda x: (x - x.mean())**2).sum()
    # Interaction
    ssinter = sstotal - (sst + mtime.loc[0, 'SS'] + mbetw.loc[0, 'SS'])
    sswg = mtime.loc[1, 'SS'] - ssinter
    sseb = sstotal - (mtime.loc[0, 'SS'] + mbetw.loc[0, 'SS'] + sswg + ssinter)

    # DEGREES OF FREEDOM
    n_obs = data.groupby(within)[dv].count().max()
    dftime = mtime.loc[0, 'DF']
    dfbetween = mbetw.loc[0, 'DF']
    dfeb = n_obs - data.groupby(between)[dv].count().count()
    dfwg = dftime * dfeb
    dfinter = mtime.loc[0, 'DF'] * mbetw.loc[0, 'DF']

    # MEAN SQUARES
    mseb = sseb / dfeb
    mswg = sswg / dfwg
    msinter = ssinter / dfinter

    # F VALUES
    fbetween = mbetw.loc[0, 'MS'] / mseb
    ftime = mtime.loc[0, 'MS'] / mswg
    finter = msinter / mswg

    # P-values
    pbetween = f(dfbetween, dfeb).sf(fbetween)
    ptime = f(dftime, dfwg).sf(ftime)
    pinter = f(dfinter, dfwg).sf(finter)

    # Effects sizes
    npsq_between = fbetween * dfbetween / (fbetween * dfbetween + dfeb)
    npsq_time = ftime * dftime / (ftime * dftime + dfwg)
    npsq_inter = ssinter / (ssinter + sswg)

    # Stats table
    aov = pd.concat([mbetw.drop(1), mtime.drop(1)], sort=False,
                    ignore_index=True)
    # Update values
    aov.rename(columns={'DF': 'DF1'}, inplace=True)
    aov.loc[0, 'F'], aov.loc[1, 'F'] = fbetween, ftime
    aov.loc[0, 'p-unc'], aov.loc[1, 'p-unc'] = pbetween, ptime
    aov.loc[0, 'np2'], aov.loc[1, 'np2'] = npsq_between, npsq_time
    aov = aov.append({'Source': 'Interaction',
                      'SS': ssinter,
                      'DF1': dfinter,
                      'MS': msinter,
                      'F': finter,
                      'p-unc': pinter,
                      'np2': npsq_inter,
                      }, ignore_index=True)

    aov['SS'] = aov['SS'].round(3)
    aov['MS'] = aov['MS'].round(3)
    aov['DF2'] = [dfeb, dfwg, dfwg]
    aov['eps'] = [np.nan, mtime.loc[0, 'eps'], np.nan]
    col_order = ['Source', 'SS', 'DF1', 'DF2', 'MS', 'F', 'p-unc',
                 'p-GG-corr', 'np2', 'eps', 'sphericity', 'W-Mauchly',
                 'p-Mauchly']

    # Replace NaN
    aov = aov.fillna('-')

    aov = aov.reindex(columns=col_order)
    aov.dropna(how='all', axis=1, inplace=True)

    # Round
    aov[['F', 'eps', 'np2']] = aov[['F', 'eps', 'np2']].round(3)

    # Export to .csv
    if export_filename is not None:
        _export_table(aov, export_filename)
    return aov
