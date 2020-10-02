from matplotlib import pyplot as plt

from akangatu.ddstep import DDStep
from melime.explainers.explainer import Explainer
from melime.explainers.visualizations.plot_importance import ExplainGraph
from melime.generators.kde_gen import KDEGen
from transf.absdata import AbsData


class Explain(DDStep):
    def _process_(self, data: AbsData):
        inner = data.inner
        generator = KDEGen(verbose=True).fit(inner.X)
        explainer = Explainer(
            model_predict=data.p,
            generator=generator,
            local_model='Ridge',
            feature_names=data.Xd,
            target_names=data.Yd
        )
        explanation, counterfactual_examples = explainer.explain_instance(
            x_explain=data.X.reshape(1, -1),
            class_index=1,
            r=1.0,
            n_samples=500,
            tol_importance=0.1,
            tol_error=0.1,
            local_mini_batch_max=40,
            scale_data=False,
            weight_kernel='gaussian'
        )
        fig, axs = ExplainGraph.plot(explanation.explain())
        plt.savefig(f'iris_x_{data.X}_m-lime_kde.svg')
        fig, axs = ExplainGraph.plot_errors(explanation)
