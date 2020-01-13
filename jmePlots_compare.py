#!/usr/bin/env python
import argparse, os, ROOT

from common.utils import *

from common.plot_style import apply_style as load_plot_style

def TH1_keys(tdirectory, prefix='', contains_all=[], contains_one=[]):

    th1_keys = []

    for k_key in tdirectory.GetListOfKeys():
        k_key_name = k_key.GetName()

        k_obj = tdirectory.Get(k_key_name)
        if not k_obj: continue

        if k_obj.InheritsFrom('TDirectory'):

           th1_keys += TH1_keys(k_obj, prefix=prefix+k_obj.GetName()+'/', contains_all=contains_all, contains_one=contains_one)

        elif k_obj.InheritsFrom('TH1'):

           h_name = prefix+k_obj.GetName()

           if len(contains_all) > 0:
              skip = False
              for _tmp in contains_all:
                  if _tmp not in h_name: skip = True; break;
              if skip: continue

           if len(contains_one) > 0:
              skip = True
              for _tmp in contains_one:
                  if _tmp in h_name: skip = False; break;
              if skip: continue

           th1_keys += [prefix+k_obj.GetName()]

    return th1_keys

def add_TH1_objects(filelist, contains_all):

    th1_dict = {}

    for i_inputf_path in filelist:

        i_inptfile = ROOT.TFile.Open(i_inputf_path)
        if (not i_inptfile) or i_inptfile.IsZombie() or i_inptfile.TestBit(ROOT.TFile.kRecovered): raise SystemExit(1)

        for h_key in TH1_keys(i_inptfile, contains_all=contains_all):

            if h_key in th1_dict:
               KILL(log_prx+'input error -> key "'+h_key+'" already exists in histogram-dictionary')

            h0 = i_inptfile.Get(h_key)
            if not (h0 and h0.InheritsFrom('TH1')):
               KILL(log_prc+'input error -- key "'+h_key+'" not associated to a TH1 object: '+opts.input)

            h_key_dict = h_key
#            h_key_dict = '/'.join(h_key.split('/')[2:])

            if h_key_dict in th1_dict: th1_dict[h_key_dict].Add(h0)
            else                     : th1_dict[h_key_dict] =   h0.Clone(); th1_dict[h_key_dict].SetDirectory(0);

            if opts.verbose: print '\033[1m'+'\033[92m'+'[input]'+'\033[0m', h_key

        ROOT.gROOT.GetListOfFiles().Remove(i_inptfile)
        i_inptfile.Close()

    return th1_dict

def get_text(x1ndc_, y1ndc_, talign_, tsize_, text_):
    txt = ROOT.TLatex(x1ndc_, y1ndc_, text_)
    txt.SetTextAlign(talign_)
    txt.SetTextSize(tsize_)
    txt.SetTextFont(42)
    txt.SetNDC()

    return txt

def plot_canvas(key, target, reference, target_legend, reference_legend, output, output_extensions):

    if (target != None) and (reference != None):
       if target.ClassName() != reference.ClassName():
          WARNING(output)
          return 1

    if   (target is not None) and (reference is not None): h_refe = reference.Clone(); h_targ = target   .Clone();
    elif (target is     None) and (reference is not None): h_refe = reference.Clone(); h_targ = reference.Clone(); h_targ.Reset();
    elif (target is not None) and (reference is     None): h_targ = target   .Clone(); h_refe = target   .Clone(); h_refe.Reset();
    elif (target is     None) and (reference is     None):
       return 1

    if not (h_targ.InheritsFrom('TH1F') or h_targ.InheritsFrom('TH1D')):
       return 1

    if (h_targ.GetNbinsX() == h_refe.GetNbinsX()) and (h_targ.GetNbinsY() == h_refe.GetNbinsY()):
       for i_bin in range(0, 2+(h_targ.GetNbinsX() * h_targ.GetNbinsY())):
           i_bin_targ = h_targ.GetBinContent(i_bin)
           i_bin_refe = h_refe.GetBinContent(i_bin)
           if abs(i_bin_targ - i_bin_refe) > 1e-8:
              print 'differs', output
              break
    else:
       print 'differs', output

##!!!!!!!
#    output_basename_woExt = str(output)
#    output_dirname = os.path.dirname(output_basename_woExt)
#    if not os.path.isdir(output_dirname): EXE('mkdir -p '+output_dirname)
#    print os.path.relpath(output_basename_woExt)
#    return
##!!!!!!!

    key_basename = os.path.basename(key)

    if '_wrt_' in key_basename:
       key_basename_split = key_basename.split('_wrt_')
       titleX = key_basename_split[1]
       titleY = key_basename_split[0]
       markerColor = [1, 2]
       markerSize = [1.5, 1.5]
       markerStyle = [20, 24]
       lineColor = [1, 2]
       lineWidth = [2, 2]
       draw_opt = 'ep'
       legendDraw_opt = 'ep'
    else:
       titleX = key_basename
       titleY = 'Entries'
       markerColor = [1, 2]
       markerSize = [0, 0]
       markerStyle = [20, 24]
       lineColor = [1, 2]
       lineWidth = [2, 2]
       draw_opt = 'hist,e0'
       legendDraw_opt = 'l'
       if key_basename.endswith('_pt') or key_basename.endswith('_pt0') or key_basename.endswith('_eta') or key_basename.endswith('_phi'):
          titleY += ' / Bin width'
          h_targ.Scale(1, 'width')
          h_refe.Scale(1, 'width')

    h_refe.SetBit(ROOT.TH1.kNoTitle)
    h_targ.SetBit(ROOT.TH1.kNoTitle)

    h_refe.UseCurrentStyle()
    h_targ.UseCurrentStyle()

    h_refe.SetMarkerColor(markerColor[0])
    h_refe.SetMarkerSize(markerSize[0])
    h_refe.SetMarkerStyle(markerStyle[0])
    h_refe.SetLineColor(lineColor[0])
    h_refe.SetLineWidth(lineWidth[0])

    h_targ.SetMarkerColor(markerColor[1])
    h_targ.SetMarkerSize(markerSize[1])
    h_targ.SetMarkerStyle(markerStyle[1])
    h_targ.SetLineColor(lineColor[1])
    h_targ.SetLineWidth(lineWidth[1])

#    opt_draw, opt_legd = 'hist,e', 'lep'
#    if h_refe.GetName().startswith('effic_'): opt_draw, opt_legd = 'pex0', 'pex0'

    ratio = True

    logY = False

    histo_type = None
    if   'numerator'   in h_refe.GetTitle(): histo_type = 'NUM'
    elif 'denominator' in h_refe.GetTitle(): histo_type = 'DEN'

    # normalize (numerator, denominator) histograms to unity
    if histo_type in ['NUM', 'DEN']:
       if h_refe.Integral() != 0.: h_refe.Scale(1. / h_refe.Integral())
       if h_targ.Integral() != 0.: h_targ.Scale(1. / h_targ.Integral())

    canvas = ROOT.TCanvas(key, key)
    canvas.SetGrid(1,1)
    canvas.SetTickx()
    canvas.SetTicky()

    T = canvas.GetTopMargin()
    R = canvas.GetRightMargin()
    B = canvas.GetBottomMargin()
    L = canvas.GetLeftMargin()

    ROOT.TGaxis.SetExponentOffset(-L+.50*L, 0.03, 'y')

    leg = ROOT.TLegend(L+(1-R-L)*0.00, (1-T)+T*0.05, L+(1-R-L)*1.00, (1-T)+T*0.95)
    leg.SetBorderSize(2)
    leg.SetTextFont(42)
    leg.SetFillColor(0)
    leg.AddEntry(h_targ, '#bf{Target}: '   +target_legend   , legendDraw_opt)
    leg.AddEntry(h_refe, '#bf{Reference}: '+reference_legend, legendDraw_opt)

    txt1 = None
    if   histo_type == 'NUM': txt1 = get_text((1-R)+R*0.25, (1-T), 11, .025, '[Numerator]');   txt1.SetTextAngle(-90);
    elif histo_type == 'DEN': txt1 = get_text((1-R)+R*0.25, (1-T), 11, .025, '[Denominator]'); txt1.SetTextAngle(-90);

    txt2 = None # get_text(L+(1-R-L)*0.05, B+(1-B-T)*.77, 13, .040, '')

    canvas.cd()

    hmax = 0.0
    for _tmp in [h_targ, h_refe]:
        for i_bin in range(1, _tmp.GetNbinsX()+1):
            hmax = max(hmax, (_tmp.GetBinContent(i_bin) + _tmp.GetBinError(i_bin)))

    if not ratio:

        canvas.SetTickx()
        canvas.SetTicky()

        canvas.SetLogy(logY)

        h_refe.SetStats(0)

        h_refe.SetYTitle(titleX)
        h_refe.SetYTitle(titleY)

        h_refe.Draw(draw_opt)
        h_targ.Draw(draw_opt+',same')
        h_refe.Draw('axis,same')
        if leg: leg.Draw('same')

        if txt1: txt1.Draw('same')
        if txt2: txt2.Draw('same')

#        h_refe.GetXaxis().SetRangeUser(xmin_, xmax_)

        if histo_type in ['NUM', 'DEN']:
           h_refe.GetYaxis().SetTitle('a.u.')

        if logY: h_refe.GetYaxis().SetRangeUser(.0003, .0003*((hmax/.0003)**(1./.85)))
        else   : h_refe.GetYaxis().SetRangeUser(.0001, .0001+((hmax-.0001) *(1./.85)))

    else:

        canvas.cd()

        pad1H = 0.7

        pad1 = ROOT.TPad('pad1', 'pad1', 0, 1-pad1H, 1, 1)

        pad1.SetTopMargin(pad1.GetTopMargin()/pad1H)
        pad1.SetBottomMargin(0.02)
        pad1.SetGrid(1,1)
        pad1.SetTickx()
        pad1.SetTicky()
        pad1.Draw()

        ROOT.SetOwnership(pad1, False)

        pad1.cd()
        h11 = h_refe.DrawCopy(draw_opt)
        h11.SetBit(ROOT.TH1.kNoTitle)
        h11.SetStats(0)
        h11.SetXTitle('')
        h11.SetYTitle(titleY)

        if histo_type in ['NUM', 'DEN']:
           h11.GetYaxis().SetTitle('a.u.')

        h11.GetYaxis().SetTitleSize(h11.GetYaxis().GetTitleSize()/pad1H)
        h11.GetYaxis().SetTitleOffset(h11.GetYaxis().GetTitleOffset()*pad1H)
        h11.GetXaxis().SetLabelSize(0)
        h11.GetYaxis().SetLabelSize (h11.GetYaxis().GetLabelSize() /pad1H)
        h11.GetXaxis().SetTickLength(h11.GetXaxis().GetTickLength()/pad1H)

        h_targ.Draw(draw_opt+',same')
        h11.Draw('axis,same')
        if leg: leg.Draw('same')

#        h11.GetXaxis().SetRangeUser(xmin_, xmax_)

        pad1.SetLogy(logY)

        if logY: h11.GetYaxis().SetRangeUser(.0003, .0003*((hmax/.0003)**(1./.85)))
        else   : h11.GetYaxis().SetRangeUser(.0001, .0001+((hmax-.0001) *(1./.85)))

        if txt1: txt1.SetTextSize(txt1.GetTextSize()/pad1H); txt1.Draw('same');
        if txt2: txt2.SetTextSize(txt2.GetTextSize()/pad1H); txt2.Draw('same');

        pad1.Update()

        if txt1: txt1.SetY(1.-(1.-txt1.GetY())/pad1H)
        if txt2: txt2.SetY(1.-(1.-txt2.GetY())/pad1H)

        if leg:
           leg.SetY1NDC(1.-(1.-leg.GetY1NDC())/pad1H)
           leg.SetY2NDC(1.-(1.-leg.GetY2NDC())/pad1H)
#           leg.SetY1NDC((leg.GetY1NDC()-canvas.GetBottomMargin()+pad1.GetBottomMargin())/pad1H)
#           leg.SetY2NDC((leg.GetY2NDC()-canvas.GetBottomMargin()+pad1.GetBottomMargin())/pad1H)

        canvas.cd()

        pad2 = ROOT.TPad('pad2', 'pad2', 0, 0, 1, 1-pad1H)
        pad2.SetTopMargin(0)
        pad2.SetBottomMargin(pad2.GetBottomMargin()/(1-pad1H))
        pad2.SetGrid(1,1)
        pad2.SetTickx()
        pad2.SetTicky()
        pad2.Draw()

        denom = h_refe.Clone()
        for _tmp in range(0, denom.GetNbinsX()+2): denom.SetBinError(_tmp, 0.)

        h21 = h_refe.Clone()
        h22 = h_targ.Clone()

        h21.Divide(denom)
        h22.Divide(denom)

#        for h0 in [h21, h22]:
#            for _tmp in range(0, h0.GetNbinsX()+2):
#                h0.SetBinContent(_tmp, h0.GetBinContent(b)-1.)

        ROOT.SetOwnership(pad2, False)

        pad2.cd()
        h21.SetStats(0)
#        h21.SetTitle(title_)
        h21.SetMarkerSize(0)

        h21.SetFillStyle(3017)
        h21.SetFillColor(16)

        h21.GetYaxis().SetTitle('Tar/Ref')
        h21.GetXaxis().SetTitle(titleX)
        h21.GetYaxis().CenterTitle()
        h21.GetXaxis().SetTitleSize  (h21.GetXaxis().GetTitleSize()   /(1-pad1H))
        h21.GetYaxis().SetTitleSize  (h21.GetYaxis().GetTitleSize()   /(1-pad1H))
        h21.GetXaxis().SetTitleOffset(h21.GetXaxis().GetTitleOffset()           )
        h21.GetYaxis().SetTitleOffset(h21.GetYaxis().GetTitleOffset() *(1-pad1H))
        h21.GetXaxis().SetLabelSize  (h21.GetXaxis().GetLabelSize()   /(1-pad1H))
        h21.GetYaxis().SetLabelSize  (h21.GetYaxis().GetLabelSize()   /(1-pad1H))
        h21.GetXaxis().SetLabelOffset(h21.GetXaxis().GetLabelOffset() /(1-pad1H))
        h21.GetYaxis().SetLabelOffset(h21.GetYaxis().GetLabelOffset()           )
        h21.GetXaxis().SetTickLength (h21.GetXaxis().GetTickLength()  /(1-pad1H))
        h21.GetYaxis().SetNdivisions(304)

#        h21.GetXaxis().SetRangeUser(xmin_, xmax_)

        h2max, h2min = None, None
        for h_tmp in [h21, h22]:
            for _tmp in range(1, h_tmp.GetNbinsX()+1):

                if (h21.GetBinContent(_tmp) == 0.) and (h21.GetBinLowEdge(_tmp) == h22.GetBinLowEdge(_tmp)) and (h22.GetBinContent(_tmp) == 0.): continue

                h2max = max(h2max, h_tmp.GetBinContent(_tmp)+h_tmp.GetBinError(_tmp)) if h2max is not None else h_tmp.GetBinContent(_tmp)+h_tmp.GetBinError(_tmp)
                h2min = min(h2min, h_tmp.GetBinContent(_tmp)-h_tmp.GetBinError(_tmp)) if h2min is not None else h_tmp.GetBinContent(_tmp)-h_tmp.GetBinError(_tmp)

        if (h2max is not None) and (h2min is not None):

#           h2min = min(int(h2min*101.)/100., int(h2min*99.)/100.)
#           h2max = max(int(h2max*101.)/100., int(h2max*99.)/100.)

           h21.GetYaxis().SetRangeUser(h2min, h2max)

        h21.GetYaxis().SetNdivisions(404)

        h21.Draw('e2')
        h22.Draw(draw_opt+',same')
        h21.Draw('axis,same')

    canvas.cd()
    canvas.Update()

    output_basename_woExt = str(output)

    output_dirname = os.path.dirname(output_basename_woExt)
    if not os.path.isdir(output_dirname): EXE('mkdir -p '+output_dirname)

    for i_ext in output_extensions:

        out_file = output_basename_woExt+'.'+i_ext

        canvas.SaveAs(out_file)

        print '\033[1m'+'\033[92m'+'[output]'+'\033[0m', os.path.relpath(out_file)

    canvas.Close()

    return 0
#### ----

#### main
if __name__ == '__main__':
    ### args --------------
    parser = argparse.ArgumentParser()

    parser.add_argument('-t', '--target', dest='target', required=True, nargs='+', default=[],
                        help='path to input DQM .root file')

    parser.add_argument('-r', '--reference', dest='reference', required=True, nargs='+', default=[],
                        help='path to input DQM .root file')

    parser.add_argument('--t-leg', dest='target_legend', action='store', default='Target',
                        help='text describing target file (text in legend entry)')

    parser.add_argument('--r-leg', dest='reference_legend', action='store', default='Reference',
                        help='text describing reference file (text in legend entry)')

    parser.add_argument('-o', '--output', dest='output', required=True, action='store', default=None,
                        help='path to output directory')

    parser.add_argument('--only-keys', dest='only_keys', nargs='+', default=[],
                        help='list of strings required to be in histogram key')

    parser.add_argument('-e', '--exts', dest='exts', nargs='+', default=['png'],
                        help='list of extension(s) for output file(s)')

    parser.add_argument('-v', '--verbose', dest='verbose', action='store_true', default=False,
                        help='enable verbose mode')

    opts, opts_unknown = parser.parse_known_args()
    ### -------------------

    ROOT.gROOT.SetBatch()
    ROOT.gErrorIgnoreLevel = ROOT.kWarning

    log_prx = os.path.basename(__file__)+' -- '

    ### args validation ---
#    if not os.path.isfile(opts.target):
#       KILL(log_prx+'invalid path to input .root file for "target" [-t]: '+opts.target)
#
#    if not os.path.isfile(opts.reference):
#       KILL(log_prx+'invalid path to input .root file for "reference" [-r]: '+opts.reference)

    if os.path.exists(opts.output):
       KILL(log_prx+'target path to output .root file already exists [-o]: '+opts.output)

    EXTS = list(set(opts.exts))

    ONLY_KEYS = list(set(opts.only_keys))

    if len(ONLY_KEYS):
       print '\n >>> will plot only TH1 objects containing all of the following strings in their internal path:', ONLY_KEYS, '\n'

    if len(opts_unknown) > 0:
       KILL(log_prx+'unrecognized command-line arguments: '+str(opts_unknown))
    ### -------------------

    ### input histograms --
    histo_dict_target = add_TH1_objects(filelist=opts.target   , contains_all=ONLY_KEYS)
    histo_dict_refern = add_TH1_objects(filelist=opts.reference, contains_all=ONLY_KEYS)

    ### output files (plots)
    load_plot_style()

    ROOT.TGaxis.SetMaxDigits(4)

    histo_paths_common     = sorted([_tmp for _tmp in histo_dict_target.keys() if _tmp     in histo_dict_refern])
    histo_paths_onlyTarget = sorted([_tmp for _tmp in histo_dict_target.keys() if _tmp not in histo_dict_refern])
    histo_paths_onlyRefern = sorted([_tmp for _tmp in histo_dict_refern.keys() if _tmp not in histo_dict_target])

    kwargs = {

      'target_legend': str(opts.target_legend),

      'reference_legend': str(opts.reference_legend),

      'output_extensions': EXTS,
    }

    for histo_key in histo_paths_onlyTarget:
        plot_canvas(key=histo_key, output=os.path.abspath(opts.output)+'/only_target/'+histo_key.replace(' ', '_'), target=histo_dict_target[histo_key], reference=None, **kwargs)

    for histo_key in histo_paths_onlyRefern:
        plot_canvas(key=histo_key, output=os.path.abspath(opts.output)+'/only_reference/'+histo_key.replace(' ', '_'), target=None, reference=histo_dict_refern[histo_key], **kwargs)

    for histo_key in histo_paths_common:
        plot_canvas(key=histo_key, output=os.path.abspath(opts.output)+'/'+histo_key.replace(' ', '_'), target=histo_dict_target[histo_key], reference=histo_dict_refern[histo_key], **kwargs)
    ### -------------------
