from matplotlib import pyplot as plt

from akangatu.ddstep import DDStep
from melime.explainers.explainer import Explainer
from melime.explainers.visualizations.plot_importance import ExplainGraph
from melime.generators.kde_gen import KDEGen
from transf.absdata import AbsData
from transf.mixin.noop import asNoOp


# TODO: simplify this class to be independent of the prediction of syntetic examples.
class Explain(asNoOp, DDStep):
    def __init__(self, inner=None, class_index=0):
        raise NotImplemented
        super().__init__(inner, {"class_index": class_index})
        # TODO: dar opção de selecionar a classe mais forte, mas depende de passar o modelo (issue no melime?)
        self.class_index = class_index

    def _process_(self, data: AbsData):
        inner = data.inner
        generator = KDEGen(verbose=True).fit(inner.X)
        # TODO: model_predict depende do modelo pra predizer em exemplos artificiais
        explainer = Explainer(
            model_predict=??????????????????????????????,
            generator=generator,
            local_model='Ridge',
            feature_names=data.Xd,
            target_names=data.Yd
        )
        explanation, counterfactual_examples = explainer.explain_instance(
            x_explain=data.X[0:1],
            class_index=self.class_index,
            r=1.0,
            n_samples=500,
            tol_importance=0.1,
            tol_error=0.1,
            local_mini_batch_max=40,
            scale_data=False,
            weight_kernel='gaussian'
        )
        fig, axs = ExplainGraph.plot(explanation.explain())
        # plt.savefig(f'iris_x_{",".join(data.Xd)}_m-lime_kde.svg')
        plt.show()  # pip install PyQt5==5.12.2  # plotlib is currently using agg, which is a non-GUI backend, so canno
        fig, axs = ExplainGraph.plot_errors(explanation)

        return data
