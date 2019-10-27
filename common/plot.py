#!/usr/bin/env python
import ROOT

from utils import *

def color(hexc):
    return ROOT.TColor.GetColor(hexc)

def get_text(x1ndc, y1ndc, textAlign, textSize, text):
    txt = ROOT.TLatex(x1ndc, y1ndc, text)
    txt.SetTextAlign(textAlign)
    txt.SetTextSize(textSize)
    txt.SetTextFont(42)
    txt.SetNDC()

    return txt

def get_pavetext(x1ndc, y1ndc, x2ndc, y2ndc, textSize, text):
    txt = ROOT.TPaveText(x1ndc, y1ndc, x2ndc, y2ndc, 'NDC')
#    txt.SetNDC()
    txt.SetTextSize(textSize)
    txt.SetTextFont(42)
    txt.AddText(text)

    return txt

def get_legend(x1ndc_, y1ndc_, x2ndc_, y2ndc_):
    legd = ROOT.TLegend(x1ndc_, y1ndc_, x2ndc_, y2ndc_)
    legd.SetBorderSize(0)
    legd.SetFillColor(0)
    legd.SetTextFont(42)

    return legd

def get_ymax_from_histos(hls, error=True):
    ymax = 0.

    for h in hls:
        if not h: continue

        for i in range(1, h.GetNbinsX()+1):
            if not error: y = h.GetBinContent(i)
            else: y = h.GetBinContent(i)+h.GetBinError(i)

            if y > ymax: ymax = y

    return ymax

def get_ymax_from_graphs(gls, error=True):
    ymax = 0.

    for g in gls:
        if not g: continue

        for i in range(0, g.GetN()):
            x, y = ROOT.Double(0.), ROOT.Double(0.)
            g.GetPoint(i, x, y)
            if error: y += g.GetErrorYhigh(i)

            if y > ymax: ymax = y

    return ymax

def poisson_ratio_graph(hN_, hD_, plot_empty_bins=False, plot_errX=True):

    g_ = ROOT.TGraphAsymmErrors()
    for ib_ in range(1, hN_.GetNbinsX()+1):
        if hN_.GetBinCenter(ib_) != hD_.GetBinCenter(ib_):
           KILL('poisson_ratio_graph -- bin-center values for numerator and denominator do not match')

        add_gp = hN_.GetBinContent(ib_) or plot_empty_bins

        if hD_.GetBinContent(ib_) and add_gp:
            xval =  hN_.GetBinCenter (ib_)
            xeup = (hN_.GetBinLowEdge(ib_+1) - hN_.GetBinCenter (ib_) if plot_errX else 0.)
            xedn = (hN_.GetBinCenter (ib_)   - hN_.GetBinLowEdge(ib_) if plot_errX else 0.)

            yval = hN_.GetBinContent (ib_) / hD_.GetBinContent(ib_)
            yeup = hN_.GetBinErrorUp (ib_) / hD_.GetBinContent(ib_)
            yedn = hN_.GetBinErrorLow(ib_) / hD_.GetBinContent(ib_)

            gN_ = g_.GetN()

            g_.SetPoint     (gN_, xval, yval)
            g_.SetPointError(gN_, xedn, xeup, yedn, yeup)

    g_.SetLineColor  (hN_.GetLineColor  ())
    g_.SetLineStyle  (hN_.GetLineStyle  ())
    g_.SetLineWidth  (hN_.GetLineWidth  ())
    g_.SetMarkerColor(hN_.GetMarkerColor())
    g_.SetMarkerStyle(hN_.GetMarkerStyle())
    g_.SetMarkerSize (hN_.GetMarkerSize ())
    g_.SetFillColor  (hN_.GetFillColor  ())
    g_.SetFillStyle  (hN_.GetFillStyle  ())

    g_.SetName ('gerr__'+hN_.GetName())
    g_.SetTitle('gerr__'+hN_.GetTitle())

    return g_
