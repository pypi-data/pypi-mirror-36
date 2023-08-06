// A Bison parser, made by GNU Bison 3.0.4.

// Skeleton implementation for Bison LALR(1) parsers in C++

// Copyright (C) 2002-2015 Free Software Foundation, Inc.

// This program is free software: you can redistribute it and/or modify
// it under the terms of the GNU General Public License as published by
// the Free Software Foundation, either version 3 of the License, or
// (at your option) any later version.

// This program is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU General Public License for more details.

// You should have received a copy of the GNU General Public License
// along with this program.  If not, see <http://www.gnu.org/licenses/>.

// As a special exception, you may create a larger work that contains
// part or all of the Bison parser skeleton and distribute that work
// under terms of your choice, so long as that work isn't itself a
// parser generator using the skeleton or a modified version thereof
// as a parser skeleton.  Alternatively, if you modify or redistribute
// the parser skeleton itself, you may (at your option) remove this
// special exception, which will cause the skeleton and the resulting
// Bison output files to be licensed under the GNU General Public
// License without this special exception.

// This special exception was added by the Free Software Foundation in
// version 2.2 of Bison.

// Take the name prefix into account.
#define yylex   pytypelex

// First part of user declarations.

#line 39 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:404

# ifndef YY_NULLPTR
#  if defined __cplusplus && 201103L <= __cplusplus
#   define YY_NULLPTR nullptr
#  else
#   define YY_NULLPTR 0
#  endif
# endif

#include "parser.tab.hh"

// User implementation prologue.

#line 53 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:412
// Unqualified %code blocks.
#line 34 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:413

namespace {
PyObject* DOT_STRING = PyString_FromString(".");

/* Helper functions for building up lists. */
PyObject* StartList(PyObject* item);
PyObject* AppendList(PyObject* list, PyObject* item);
PyObject* ExtendList(PyObject* dst, PyObject* src);

}  // end namespace


// Check that a python value is not NULL.  This must be a macro because it
// calls YYERROR (which is a goto).
#define CHECK(x, loc) do { if (x == NULL) {\
    ctx->SetErrorLocation(loc); \
    YYERROR; \
  }} while(0)

// pytypelex is generated in lexer.lex.cc, but because it uses semantic_type and
// location, it must be declared here.
int pytypelex(pytype::parser::semantic_type* lvalp, pytype::location* llocp,
              void* scanner);


#line 81 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:413


#ifndef YY_
# if defined YYENABLE_NLS && YYENABLE_NLS
#  if ENABLE_NLS
#   include <libintl.h> // FIXME: INFRINGES ON USER NAME SPACE.
#   define YY_(msgid) dgettext ("bison-runtime", msgid)
#  endif
# endif
# ifndef YY_
#  define YY_(msgid) msgid
# endif
#endif

#define YYRHSLOC(Rhs, K) ((Rhs)[K].location)
/* YYLLOC_DEFAULT -- Set CURRENT to span from RHS[1] to RHS[N].
   If N is 0, then set CURRENT to the empty location which ends
   the previous symbol: RHS[0] (always defined).  */

# ifndef YYLLOC_DEFAULT
#  define YYLLOC_DEFAULT(Current, Rhs, N)                               \
    do                                                                  \
      if (N)                                                            \
        {                                                               \
          (Current).begin  = YYRHSLOC (Rhs, 1).begin;                   \
          (Current).end    = YYRHSLOC (Rhs, N).end;                     \
        }                                                               \
      else                                                              \
        {                                                               \
          (Current).begin = (Current).end = YYRHSLOC (Rhs, 0).end;      \
        }                                                               \
    while (/*CONSTCOND*/ false)
# endif


// Suppress unused-variable warnings by "using" E.
#define YYUSE(E) ((void) (E))

// Enable debugging if requested.
#if YYDEBUG

// A pseudo ostream that takes yydebug_ into account.
# define YYCDEBUG if (yydebug_) (*yycdebug_)

# define YY_SYMBOL_PRINT(Title, Symbol)         \
  do {                                          \
    if (yydebug_)                               \
    {                                           \
      *yycdebug_ << Title << ' ';               \
      yy_print_ (*yycdebug_, Symbol);           \
      *yycdebug_ << std::endl;                  \
    }                                           \
  } while (false)

# define YY_REDUCE_PRINT(Rule)          \
  do {                                  \
    if (yydebug_)                       \
      yy_reduce_print_ (Rule);          \
  } while (false)

# define YY_STACK_PRINT()               \
  do {                                  \
    if (yydebug_)                       \
      yystack_print_ ();                \
  } while (false)

#else // !YYDEBUG

# define YYCDEBUG if (false) std::cerr
# define YY_SYMBOL_PRINT(Title, Symbol)  YYUSE(Symbol)
# define YY_REDUCE_PRINT(Rule)           static_cast<void>(0)
# define YY_STACK_PRINT()                static_cast<void>(0)

#endif // !YYDEBUG

#define yyerrok         (yyerrstatus_ = 0)
#define yyclearin       (yyla.clear ())

#define YYACCEPT        goto yyacceptlab
#define YYABORT         goto yyabortlab
#define YYERROR         goto yyerrorlab
#define YYRECOVERING()  (!!yyerrstatus_)

#line 17 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:479
namespace pytype {
#line 167 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:479

  /* Return YYSTR after stripping away unnecessary quotes and
     backslashes, so that it's suitable for yyerror.  The heuristic is
     that double-quoting is unnecessary unless the string contains an
     apostrophe, a comma, or backslash (other than backslash-backslash).
     YYSTR is taken from yytname.  */
  std::string
  parser::yytnamerr_ (const char *yystr)
  {
    if (*yystr == '"')
      {
        std::string yyr = "";
        char const *yyp = yystr;

        for (;;)
          switch (*++yyp)
            {
            case '\'':
            case ',':
              goto do_not_strip_quotes;

            case '\\':
              if (*++yyp != '\\')
                goto do_not_strip_quotes;
              // Fall through.
            default:
              yyr += *yyp;
              break;

            case '"':
              return yyr;
            }
      do_not_strip_quotes: ;
      }

    return yystr;
  }


  /// Build a parser object.
  parser::parser (void* scanner_yyarg, pytype::Context* ctx_yyarg)
    :
#if YYDEBUG
      yydebug_ (false),
      yycdebug_ (&std::cerr),
#endif
      scanner (scanner_yyarg),
      ctx (ctx_yyarg)
  {}

  parser::~parser ()
  {}


  /*---------------.
  | Symbol types.  |
  `---------------*/

  inline
  parser::syntax_error::syntax_error (const location_type& l, const std::string& m)
    : std::runtime_error (m)
    , location (l)
  {}

  // basic_symbol.
  template <typename Base>
  inline
  parser::basic_symbol<Base>::basic_symbol ()
    : value ()
  {}

  template <typename Base>
  inline
  parser::basic_symbol<Base>::basic_symbol (const basic_symbol& other)
    : Base (other)
    , value ()
    , location (other.location)
  {
    value = other.value;
  }


  template <typename Base>
  inline
  parser::basic_symbol<Base>::basic_symbol (typename Base::kind_type t, const semantic_type& v, const location_type& l)
    : Base (t)
    , value (v)
    , location (l)
  {}


  /// Constructor for valueless symbols.
  template <typename Base>
  inline
  parser::basic_symbol<Base>::basic_symbol (typename Base::kind_type t, const location_type& l)
    : Base (t)
    , value ()
    , location (l)
  {}

  template <typename Base>
  inline
  parser::basic_symbol<Base>::~basic_symbol ()
  {
    clear ();
  }

  template <typename Base>
  inline
  void
  parser::basic_symbol<Base>::clear ()
  {
    Base::clear ();
  }

  template <typename Base>
  inline
  bool
  parser::basic_symbol<Base>::empty () const
  {
    return Base::type_get () == empty_symbol;
  }

  template <typename Base>
  inline
  void
  parser::basic_symbol<Base>::move (basic_symbol& s)
  {
    super_type::move(s);
    value = s.value;
    location = s.location;
  }

  // by_type.
  inline
  parser::by_type::by_type ()
    : type (empty_symbol)
  {}

  inline
  parser::by_type::by_type (const by_type& other)
    : type (other.type)
  {}

  inline
  parser::by_type::by_type (token_type t)
    : type (yytranslate_ (t))
  {}

  inline
  void
  parser::by_type::clear ()
  {
    type = empty_symbol;
  }

  inline
  void
  parser::by_type::move (by_type& that)
  {
    type = that.type;
    that.clear ();
  }

  inline
  int
  parser::by_type::type_get () const
  {
    return type;
  }


  // by_state.
  inline
  parser::by_state::by_state ()
    : state (empty_state)
  {}

  inline
  parser::by_state::by_state (const by_state& other)
    : state (other.state)
  {}

  inline
  void
  parser::by_state::clear ()
  {
    state = empty_state;
  }

  inline
  void
  parser::by_state::move (by_state& that)
  {
    state = that.state;
    that.clear ();
  }

  inline
  parser::by_state::by_state (state_type s)
    : state (s)
  {}

  inline
  parser::symbol_number_type
  parser::by_state::type_get () const
  {
    if (state == empty_state)
      return empty_symbol;
    else
      return yystos_[state];
  }

  inline
  parser::stack_symbol_type::stack_symbol_type ()
  {}


  inline
  parser::stack_symbol_type::stack_symbol_type (state_type s, symbol_type& that)
    : super_type (s, that.location)
  {
    value = that.value;
    // that is emptied.
    that.type = empty_symbol;
  }

  inline
  parser::stack_symbol_type&
  parser::stack_symbol_type::operator= (const stack_symbol_type& that)
  {
    state = that.state;
    value = that.value;
    location = that.location;
    return *this;
  }


  template <typename Base>
  inline
  void
  parser::yy_destroy_ (const char* yymsg, basic_symbol<Base>& yysym) const
  {
    if (yymsg)
      YY_SYMBOL_PRINT (yymsg, yysym);

    // User destructor.
    switch (yysym.type_get ())
    {
            case 3: // NAME

#line 99 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:614
        { Py_CLEAR((yysym.value.obj)); }
#line 421 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:614
        break;

      case 4: // NUMBER

#line 99 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:614
        { Py_CLEAR((yysym.value.obj)); }
#line 428 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:614
        break;

      case 5: // LEXERROR

#line 99 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:614
        { Py_CLEAR((yysym.value.obj)); }
#line 435 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:614
        break;

      case 47: // start

#line 99 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:614
        { Py_CLEAR((yysym.value.obj)); }
#line 442 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:614
        break;

      case 48: // unit

#line 99 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:614
        { Py_CLEAR((yysym.value.obj)); }
#line 449 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:614
        break;

      case 49: // alldefs

#line 99 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:614
        { Py_CLEAR((yysym.value.obj)); }
#line 456 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:614
        break;

      case 51: // classdef

#line 99 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:614
        { Py_CLEAR((yysym.value.obj)); }
#line 463 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:614
        break;

      case 52: // class_name

#line 99 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:614
        { Py_CLEAR((yysym.value.obj)); }
#line 470 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:614
        break;

      case 53: // parents

#line 99 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:614
        { Py_CLEAR((yysym.value.obj)); }
#line 477 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:614
        break;

      case 54: // parent_list

#line 99 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:614
        { Py_CLEAR((yysym.value.obj)); }
#line 484 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:614
        break;

      case 55: // parent

#line 99 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:614
        { Py_CLEAR((yysym.value.obj)); }
#line 491 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:614
        break;

      case 56: // maybe_class_funcs

#line 99 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:614
        { Py_CLEAR((yysym.value.obj)); }
#line 498 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:614
        break;

      case 57: // class_funcs

#line 99 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:614
        { Py_CLEAR((yysym.value.obj)); }
#line 505 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:614
        break;

      case 58: // funcdefs

#line 99 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:614
        { Py_CLEAR((yysym.value.obj)); }
#line 512 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:614
        break;

      case 59: // if_stmt

#line 99 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:614
        { Py_CLEAR((yysym.value.obj)); }
#line 519 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:614
        break;

      case 60: // if_and_elifs

#line 99 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:614
        { Py_CLEAR((yysym.value.obj)); }
#line 526 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:614
        break;

      case 61: // class_if_stmt

#line 99 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:614
        { Py_CLEAR((yysym.value.obj)); }
#line 533 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:614
        break;

      case 62: // class_if_and_elifs

#line 99 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:614
        { Py_CLEAR((yysym.value.obj)); }
#line 540 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:614
        break;

      case 63: // if_cond

#line 99 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:614
        { Py_CLEAR((yysym.value.obj)); }
#line 547 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:614
        break;

      case 64: // elif_cond

#line 99 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:614
        { Py_CLEAR((yysym.value.obj)); }
#line 554 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:614
        break;

      case 65: // else_cond

#line 99 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:614
        { Py_CLEAR((yysym.value.obj)); }
#line 561 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:614
        break;

      case 66: // condition

#line 99 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:614
        { Py_CLEAR((yysym.value.obj)); }
#line 568 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:614
        break;

      case 67: // version_tuple

#line 99 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:614
        { Py_CLEAR((yysym.value.obj)); }
#line 575 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:614
        break;

      case 68: // condition_op

#line 99 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:614
        { Py_CLEAR((yysym.value.str)); }
#line 582 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:614
        break;

      case 69: // constantdef

#line 99 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:614
        { Py_CLEAR((yysym.value.obj)); }
#line 589 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:614
        break;

      case 70: // importdef

#line 99 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:614
        { Py_CLEAR((yysym.value.obj)); }
#line 596 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:614
        break;

      case 71: // import_items

#line 99 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:614
        { Py_CLEAR((yysym.value.obj)); }
#line 603 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:614
        break;

      case 72: // import_item

#line 99 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:614
        { Py_CLEAR((yysym.value.obj)); }
#line 610 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:614
        break;

      case 73: // import_name

#line 99 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:614
        { Py_CLEAR((yysym.value.obj)); }
#line 617 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:614
        break;

      case 74: // from_list

#line 99 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:614
        { Py_CLEAR((yysym.value.obj)); }
#line 624 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:614
        break;

      case 75: // from_items

#line 99 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:614
        { Py_CLEAR((yysym.value.obj)); }
#line 631 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:614
        break;

      case 76: // from_item

#line 99 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:614
        { Py_CLEAR((yysym.value.obj)); }
#line 638 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:614
        break;

      case 77: // alias_or_constant

#line 99 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:614
        { Py_CLEAR((yysym.value.obj)); }
#line 645 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:614
        break;

      case 78: // typevardef

#line 99 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:614
        { Py_CLEAR((yysym.value.obj)); }
#line 652 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:614
        break;

      case 79: // typevar_args

#line 99 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:614
        { Py_CLEAR((yysym.value.obj)); }
#line 659 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:614
        break;

      case 80: // typevar_kwargs

#line 99 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:614
        { Py_CLEAR((yysym.value.obj)); }
#line 666 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:614
        break;

      case 81: // typevar_kwarg

#line 99 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:614
        { Py_CLEAR((yysym.value.obj)); }
#line 673 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:614
        break;

      case 82: // funcdef

#line 99 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:614
        { Py_CLEAR((yysym.value.obj)); }
#line 680 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:614
        break;

      case 83: // decorators

#line 99 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:614
        { Py_CLEAR((yysym.value.obj)); }
#line 687 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:614
        break;

      case 84: // decorator

#line 99 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:614
        { Py_CLEAR((yysym.value.obj)); }
#line 694 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:614
        break;

      case 85: // params

#line 99 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:614
        { Py_CLEAR((yysym.value.obj)); }
#line 701 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:614
        break;

      case 86: // param_list

#line 99 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:614
        { Py_CLEAR((yysym.value.obj)); }
#line 708 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:614
        break;

      case 87: // param

#line 99 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:614
        { Py_CLEAR((yysym.value.obj)); }
#line 715 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:614
        break;

      case 88: // param_type

#line 99 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:614
        { Py_CLEAR((yysym.value.obj)); }
#line 722 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:614
        break;

      case 89: // param_default

#line 99 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:614
        { Py_CLEAR((yysym.value.obj)); }
#line 729 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:614
        break;

      case 90: // param_star_name

#line 99 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:614
        { Py_CLEAR((yysym.value.obj)); }
#line 736 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:614
        break;

      case 91: // return

#line 99 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:614
        { Py_CLEAR((yysym.value.obj)); }
#line 743 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:614
        break;

      case 93: // maybe_body

#line 99 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:614
        { Py_CLEAR((yysym.value.obj)); }
#line 750 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:614
        break;

      case 95: // body

#line 99 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:614
        { Py_CLEAR((yysym.value.obj)); }
#line 757 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:614
        break;

      case 96: // body_stmt

#line 99 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:614
        { Py_CLEAR((yysym.value.obj)); }
#line 764 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:614
        break;

      case 97: // type_parameters

#line 99 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:614
        { Py_CLEAR((yysym.value.obj)); }
#line 771 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:614
        break;

      case 98: // type_parameter

#line 99 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:614
        { Py_CLEAR((yysym.value.obj)); }
#line 778 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:614
        break;

      case 99: // type

#line 99 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:614
        { Py_CLEAR((yysym.value.obj)); }
#line 785 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:614
        break;

      case 100: // named_tuple_fields

#line 99 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:614
        { Py_CLEAR((yysym.value.obj)); }
#line 792 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:614
        break;

      case 101: // named_tuple_field_list

#line 99 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:614
        { Py_CLEAR((yysym.value.obj)); }
#line 799 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:614
        break;

      case 102: // named_tuple_field

#line 99 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:614
        { Py_CLEAR((yysym.value.obj)); }
#line 806 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:614
        break;

      case 104: // maybe_type_list

#line 99 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:614
        { Py_CLEAR((yysym.value.obj)); }
#line 813 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:614
        break;

      case 105: // type_list

#line 99 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:614
        { Py_CLEAR((yysym.value.obj)); }
#line 820 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:614
        break;

      case 106: // type_tuple_elements

#line 99 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:614
        { Py_CLEAR((yysym.value.obj)); }
#line 827 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:614
        break;

      case 107: // type_tuple_literal

#line 99 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:614
        { Py_CLEAR((yysym.value.obj)); }
#line 834 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:614
        break;

      case 108: // dotted_name

#line 99 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:614
        { Py_CLEAR((yysym.value.obj)); }
#line 841 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:614
        break;

      case 109: // getitem_key

#line 99 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:614
        { Py_CLEAR((yysym.value.obj)); }
#line 848 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:614
        break;

      case 110: // maybe_number

#line 99 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:614
        { Py_CLEAR((yysym.value.obj)); }
#line 855 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:614
        break;


      default:
        break;
    }
  }

#if YYDEBUG
  template <typename Base>
  void
  parser::yy_print_ (std::ostream& yyo,
                                     const basic_symbol<Base>& yysym) const
  {
    std::ostream& yyoutput = yyo;
    YYUSE (yyoutput);
    symbol_number_type yytype = yysym.type_get ();
    // Avoid a (spurious) G++ 4.8 warning about "array subscript is
    // below array bounds".
    if (yysym.empty ())
      std::abort ();
    yyo << (yytype < yyntokens_ ? "token" : "nterm")
        << ' ' << yytname_[yytype] << " ("
        << yysym.location << ": ";
    YYUSE (yytype);
    yyo << ')';
  }
#endif

  inline
  void
  parser::yypush_ (const char* m, state_type s, symbol_type& sym)
  {
    stack_symbol_type t (s, sym);
    yypush_ (m, t);
  }

  inline
  void
  parser::yypush_ (const char* m, stack_symbol_type& s)
  {
    if (m)
      YY_SYMBOL_PRINT (m, s);
    yystack_.push (s);
  }

  inline
  void
  parser::yypop_ (unsigned int n)
  {
    yystack_.pop (n);
  }

#if YYDEBUG
  std::ostream&
  parser::debug_stream () const
  {
    return *yycdebug_;
  }

  void
  parser::set_debug_stream (std::ostream& o)
  {
    yycdebug_ = &o;
  }


  parser::debug_level_type
  parser::debug_level () const
  {
    return yydebug_;
  }

  void
  parser::set_debug_level (debug_level_type l)
  {
    yydebug_ = l;
  }
#endif // YYDEBUG

  inline parser::state_type
  parser::yy_lr_goto_state_ (state_type yystate, int yysym)
  {
    int yyr = yypgoto_[yysym - yyntokens_] + yystate;
    if (0 <= yyr && yyr <= yylast_ && yycheck_[yyr] == yystate)
      return yytable_[yyr];
    else
      return yydefgoto_[yysym - yyntokens_];
  }

  inline bool
  parser::yy_pact_value_is_default_ (int yyvalue)
  {
    return yyvalue == yypact_ninf_;
  }

  inline bool
  parser::yy_table_value_is_error_ (int yyvalue)
  {
    return yyvalue == yytable_ninf_;
  }

  int
  parser::parse ()
  {
    // State.
    int yyn;
    /// Length of the RHS of the rule being reduced.
    int yylen = 0;

    // Error handling.
    int yynerrs_ = 0;
    int yyerrstatus_ = 0;

    /// The lookahead symbol.
    symbol_type yyla;

    /// The locations where the error started and ended.
    stack_symbol_type yyerror_range[3];

    /// The return value of parse ().
    int yyresult;

    // FIXME: This shoud be completely indented.  It is not yet to
    // avoid gratuitous conflicts when merging into the master branch.
    try
      {
    YYCDEBUG << "Starting parse" << std::endl;


    /* Initialize the stack.  The initial state will be set in
       yynewstate, since the latter expects the semantical and the
       location values to have been already stored, initialize these
       stacks with a primary value.  */
    yystack_.clear ();
    yypush_ (YY_NULLPTR, 0, yyla);

    // A new symbol was pushed on the stack.
  yynewstate:
    YYCDEBUG << "Entering state " << yystack_[0].state << std::endl;

    // Accept?
    if (yystack_[0].state == yyfinal_)
      goto yyacceptlab;

    goto yybackup;

    // Backup.
  yybackup:

    // Try to take a decision without lookahead.
    yyn = yypact_[yystack_[0].state];
    if (yy_pact_value_is_default_ (yyn))
      goto yydefault;

    // Read a lookahead token.
    if (yyla.empty ())
      {
        YYCDEBUG << "Reading a token: ";
        try
          {
            yyla.type = yytranslate_ (yylex (&yyla.value, &yyla.location, scanner));
          }
        catch (const syntax_error& yyexc)
          {
            error (yyexc);
            goto yyerrlab1;
          }
      }
    YY_SYMBOL_PRINT ("Next token is", yyla);

    /* If the proper action on seeing token YYLA.TYPE is to reduce or
       to detect an error, take that action.  */
    yyn += yyla.type_get ();
    if (yyn < 0 || yylast_ < yyn || yycheck_[yyn] != yyla.type_get ())
      goto yydefault;

    // Reduce or error.
    yyn = yytable_[yyn];
    if (yyn <= 0)
      {
        if (yy_table_value_is_error_ (yyn))
          goto yyerrlab;
        yyn = -yyn;
        goto yyreduce;
      }

    // Count tokens shifted since error; after three, turn off error status.
    if (yyerrstatus_)
      --yyerrstatus_;

    // Shift the lookahead token.
    yypush_ ("Shifting", yyn, yyla);
    goto yynewstate;

  /*-----------------------------------------------------------.
  | yydefault -- do the default action for the current state.  |
  `-----------------------------------------------------------*/
  yydefault:
    yyn = yydefact_[yystack_[0].state];
    if (yyn == 0)
      goto yyerrlab;
    goto yyreduce;

  /*-----------------------------.
  | yyreduce -- Do a reduction.  |
  `-----------------------------*/
  yyreduce:
    yylen = yyr2_[yyn];
    {
      stack_symbol_type yylhs;
      yylhs.state = yy_lr_goto_state_(yystack_[yylen].state, yyr1_[yyn]);
      /* If YYLEN is nonzero, implement the default value of the
         action: '$$ = $1'.  Otherwise, use the top of the stack.

         Otherwise, the following line sets YYLHS.VALUE to garbage.
         This behavior is undocumented and Bison users should not rely
         upon it.  */
      if (yylen)
        yylhs.value = yystack_[yylen - 1].value;
      else
        yylhs.value = yystack_[0].value;

      // Compute the default @$.
      {
        slice<stack_symbol_type, stack_type> slice (yystack_, yylen);
        YYLLOC_DEFAULT (yylhs.location, slice, yylen);
      }

      // Perform the reduction.
      YY_REDUCE_PRINT (yyn);
      try
        {
          switch (yyn)
            {
  case 2:
#line 132 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { ctx->SetAndDelResult((yystack_[1].value.obj)); (yylhs.value.obj) = NULL; }
#line 1094 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 3:
#line 133 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { ctx->SetAndDelResult((yystack_[1].value.obj)); (yylhs.value.obj) = NULL; }
#line 1100 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 5:
#line 141 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = AppendList((yystack_[1].value.obj), (yystack_[0].value.obj)); }
#line 1106 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 6:
#line 142 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = AppendList((yystack_[1].value.obj), (yystack_[0].value.obj)); }
#line 1112 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 7:
#line 143 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = (yystack_[1].value.obj); Py_DECREF((yystack_[0].value.obj)); }
#line 1118 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 8:
#line 144 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    {
      (yylhs.value.obj) = (yystack_[1].value.obj);
      PyObject* tmp = ctx->Call(kAddAliasOrConstant, "(N)", (yystack_[0].value.obj));
      CHECK(tmp, yylhs.location);
      Py_DECREF(tmp);
    }
#line 1129 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 9:
#line 150 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = AppendList((yystack_[1].value.obj), (yystack_[0].value.obj)); }
#line 1135 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 10:
#line 151 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = (yystack_[1].value.obj); Py_DECREF((yystack_[0].value.obj)); }
#line 1141 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 11:
#line 152 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    {
      PyObject* tmp = ctx->Call(kIfEnd, "(N)", (yystack_[0].value.obj));
      CHECK(tmp, yystack_[0].location);
      (yylhs.value.obj) = ExtendList((yystack_[1].value.obj), tmp);
    }
#line 1151 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 12:
#line 157 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = PyList_New(0); }
#line 1157 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 15:
#line 168 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    {
      (yylhs.value.obj) = ctx->Call(kNewClass, "(NNN)", (yystack_[4].value.obj), (yystack_[3].value.obj), (yystack_[0].value.obj));
      CHECK((yylhs.value.obj), yylhs.location);
    }
#line 1166 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 16:
#line 175 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    {
      // Do not borrow the $1 reference since it is also returned later
      // in $$.  Use O instead of N in the format string.
      PyObject* tmp = ctx->Call(kRegisterClassName, "(O)", (yystack_[0].value.obj));
      CHECK(tmp, yylhs.location);
      Py_DECREF(tmp);
      (yylhs.value.obj) = (yystack_[0].value.obj);
    }
#line 1179 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 17:
#line 186 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = (yystack_[1].value.obj); }
#line 1185 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 18:
#line 187 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = PyList_New(0); }
#line 1191 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 19:
#line 188 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = PyList_New(0); }
#line 1197 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 20:
#line 192 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = AppendList((yystack_[2].value.obj), (yystack_[0].value.obj)); }
#line 1203 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 21:
#line 193 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = StartList((yystack_[0].value.obj)); }
#line 1209 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 22:
#line 197 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = (yystack_[0].value.obj); }
#line 1215 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 23:
#line 198 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = Py_BuildValue("(NN)", (yystack_[2].value.obj), (yystack_[0].value.obj)); }
#line 1221 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 24:
#line 202 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = PyList_New(0); }
#line 1227 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 25:
#line 203 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = (yystack_[1].value.obj); }
#line 1233 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 26:
#line 204 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = (yystack_[1].value.obj); }
#line 1239 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 27:
#line 208 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = PyList_New(0); }
#line 1245 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 29:
#line 213 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = AppendList((yystack_[1].value.obj), (yystack_[0].value.obj)); }
#line 1251 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 30:
#line 214 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    {
      PyObject* tmp = ctx->Call(kNewAliasOrConstant, "(N)", (yystack_[0].value.obj));
      CHECK(tmp, yylhs.location);
      (yylhs.value.obj) = AppendList((yystack_[1].value.obj), tmp);
    }
#line 1261 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 31:
#line 219 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = AppendList((yystack_[1].value.obj), (yystack_[0].value.obj)); }
#line 1267 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 32:
#line 220 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    {
      PyObject* tmp = ctx->Call(kIfEnd, "(N)", (yystack_[0].value.obj));
      CHECK(tmp, yystack_[0].location);
      (yylhs.value.obj) = ExtendList((yystack_[1].value.obj), tmp);
    }
#line 1277 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 33:
#line 225 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = AppendList((yystack_[1].value.obj), (yystack_[0].value.obj)); }
#line 1283 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 34:
#line 226 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = PyList_New(0); }
#line 1289 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 35:
#line 231 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    {
      (yylhs.value.obj) = AppendList((yystack_[5].value.obj), Py_BuildValue("(NN)", (yystack_[4].value.obj), (yystack_[1].value.obj)));
    }
#line 1297 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 37:
#line 239 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    {
      (yylhs.value.obj) = Py_BuildValue("[(NN)]", (yystack_[4].value.obj), (yystack_[1].value.obj));
    }
#line 1305 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 38:
#line 243 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    {
      (yylhs.value.obj) = AppendList((yystack_[5].value.obj), Py_BuildValue("(NN)", (yystack_[4].value.obj), (yystack_[1].value.obj)));
    }
#line 1313 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 39:
#line 262 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    {
      (yylhs.value.obj) = AppendList((yystack_[5].value.obj), Py_BuildValue("(NN)", (yystack_[4].value.obj), (yystack_[1].value.obj)));
    }
#line 1321 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 41:
#line 270 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    {
      (yylhs.value.obj) = Py_BuildValue("[(NN)]", (yystack_[4].value.obj), (yystack_[1].value.obj));
    }
#line 1329 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 42:
#line 274 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    {
      (yylhs.value.obj) = AppendList((yystack_[5].value.obj), Py_BuildValue("(NN)", (yystack_[4].value.obj), (yystack_[1].value.obj)));
    }
#line 1337 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 43:
#line 286 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = ctx->Call(kIfBegin, "(N)", (yystack_[0].value.obj)); CHECK((yylhs.value.obj), yylhs.location); }
#line 1343 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 44:
#line 290 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = ctx->Call(kIfElif, "(N)", (yystack_[0].value.obj)); CHECK((yylhs.value.obj), yylhs.location); }
#line 1349 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 45:
#line 294 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = ctx->Call(kIfElse, "()"); CHECK((yylhs.value.obj), yylhs.location); }
#line 1355 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 46:
#line 298 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    {
      (yylhs.value.obj) = Py_BuildValue("((NO)sN)", (yystack_[2].value.obj), Py_None, (yystack_[1].value.str), (yystack_[0].value.obj));
    }
#line 1363 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 47:
#line 301 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    {
      (yylhs.value.obj) = Py_BuildValue("((NO)sN)", (yystack_[2].value.obj), Py_None, (yystack_[1].value.str), (yystack_[0].value.obj));
    }
#line 1371 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 48:
#line 304 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    {
      (yylhs.value.obj) = Py_BuildValue("((NN)sN)", (yystack_[5].value.obj), (yystack_[3].value.obj), (yystack_[1].value.str), (yystack_[0].value.obj));
    }
#line 1379 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 49:
#line 307 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    {
      (yylhs.value.obj) = Py_BuildValue("((NN)sN)", (yystack_[5].value.obj), (yystack_[3].value.obj), (yystack_[1].value.str), (yystack_[0].value.obj));
    }
#line 1387 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 50:
#line 310 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = Py_BuildValue("(NsN)", (yystack_[2].value.obj), "and", (yystack_[0].value.obj)); }
#line 1393 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 51:
#line 311 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = Py_BuildValue("(NsN)", (yystack_[2].value.obj), "or", (yystack_[0].value.obj)); }
#line 1399 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 52:
#line 312 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = (yystack_[1].value.obj); }
#line 1405 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 53:
#line 317 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = Py_BuildValue("(N)", (yystack_[2].value.obj)); }
#line 1411 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 54:
#line 318 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = Py_BuildValue("(NN)", (yystack_[3].value.obj), (yystack_[1].value.obj)); }
#line 1417 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 55:
#line 319 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    {
      (yylhs.value.obj) = Py_BuildValue("(NNN)", (yystack_[5].value.obj), (yystack_[3].value.obj), (yystack_[1].value.obj));
    }
#line 1425 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 56:
#line 325 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.str) = "<"; }
#line 1431 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 57:
#line 326 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.str) = ">"; }
#line 1437 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 58:
#line 327 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.str) = "<="; }
#line 1443 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 59:
#line 328 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.str) = ">="; }
#line 1449 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 60:
#line 329 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.str) = "=="; }
#line 1455 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 61:
#line 330 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.str) = "!="; }
#line 1461 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 62:
#line 334 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    {
      (yylhs.value.obj) = ctx->Call(kNewConstant, "(NN)", (yystack_[2].value.obj), (yystack_[0].value.obj));
      CHECK((yylhs.value.obj), yylhs.location);
    }
#line 1470 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 63:
#line 338 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    {
      (yylhs.value.obj) = ctx->Call(kNewConstant, "(NN)", (yystack_[2].value.obj), ctx->Value(kByteString));
      CHECK((yylhs.value.obj), yylhs.location);
    }
#line 1479 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 64:
#line 342 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    {
      (yylhs.value.obj) = ctx->Call(kNewConstant, "(NN)", (yystack_[2].value.obj), ctx->Value(kUnicodeString));
      CHECK((yylhs.value.obj), yylhs.location);
    }
#line 1488 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 65:
#line 346 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    {
      (yylhs.value.obj) = ctx->Call(kNewConstant, "(NN)", (yystack_[2].value.obj), (yystack_[0].value.obj));
      CHECK((yylhs.value.obj), yylhs.location);
    }
#line 1497 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 66:
#line 350 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    {
      (yylhs.value.obj) = ctx->Call(kNewConstant, "(NN)", (yystack_[2].value.obj), ctx->Value(kAnything));
      CHECK((yylhs.value.obj), yylhs.location);
    }
#line 1506 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 67:
#line 354 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    {
      (yylhs.value.obj) = ctx->Call(kNewConstant, "(NN)", (yystack_[5].value.obj), (yystack_[1].value.obj));
      CHECK((yylhs.value.obj), yylhs.location);
    }
#line 1515 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 68:
#line 358 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    {
      (yylhs.value.obj) = ctx->Call(kNewConstant, "(NN)", (yystack_[3].value.obj), (yystack_[1].value.obj));
      CHECK((yylhs.value.obj), yylhs.location);
    }
#line 1524 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 69:
#line 362 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    {
      (yylhs.value.obj) = ctx->Call(kNewConstant, "(NN)", (yystack_[5].value.obj), (yystack_[3].value.obj));
      CHECK((yylhs.value.obj), yylhs.location);
    }
#line 1533 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 70:
#line 369 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    {
      (yylhs.value.obj) = ctx->Call(kAddImport, "(ON)", Py_None, (yystack_[0].value.obj));
      CHECK((yylhs.value.obj), yylhs.location);
    }
#line 1542 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 71:
#line 373 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    {
      (yylhs.value.obj) = ctx->Call(kAddImport, "(NN)", (yystack_[2].value.obj), (yystack_[0].value.obj));
      CHECK((yylhs.value.obj), yylhs.location);
    }
#line 1551 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 72:
#line 377 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    {
      // Special-case "from . import" and pass in a __PACKAGE__ token that
      // the Python parser code will rewrite to the current package name.
      (yylhs.value.obj) = ctx->Call(kAddImport, "(sN)", "__PACKAGE__", (yystack_[0].value.obj));
      CHECK((yylhs.value.obj), yylhs.location);
    }
#line 1562 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 73:
#line 386 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = AppendList((yystack_[2].value.obj), (yystack_[0].value.obj)); }
#line 1568 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 74:
#line 387 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = StartList((yystack_[0].value.obj)); }
#line 1574 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 76:
#line 391 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = Py_BuildValue("(NN)", (yystack_[2].value.obj), (yystack_[0].value.obj)); }
#line 1580 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 78:
#line 397 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    {
      (yylhs.value.obj) = PyString_FromFormat(".%s", PyString_AsString((yystack_[0].value.obj)));
      Py_DECREF((yystack_[0].value.obj));
    }
#line 1589 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 80:
#line 405 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = (yystack_[1].value.obj); }
#line 1595 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 81:
#line 406 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = (yystack_[2].value.obj); }
#line 1601 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 82:
#line 410 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = AppendList((yystack_[2].value.obj), (yystack_[0].value.obj)); }
#line 1607 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 83:
#line 411 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = StartList((yystack_[0].value.obj)); }
#line 1613 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 85:
#line 416 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    {
 (yylhs.value.obj) = PyString_FromString("NamedTuple");
 }
#line 1621 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 86:
#line 419 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    {
 (yylhs.value.obj) = PyString_FromString("TypeVar");
 }
#line 1629 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 87:
#line 422 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    {
 (yylhs.value.obj) = PyString_FromString("*");
 }
#line 1637 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 88:
#line 425 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = Py_BuildValue("(NN)", (yystack_[2].value.obj), (yystack_[0].value.obj)); }
#line 1643 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 89:
#line 429 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = Py_BuildValue("(NN)", (yystack_[2].value.obj), (yystack_[0].value.obj)); }
#line 1649 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 90:
#line 433 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    {
      (yylhs.value.obj) = ctx->Call(kAddTypeVar, "(NNN)", (yystack_[6].value.obj), (yystack_[2].value.obj), (yystack_[1].value.obj));
      CHECK((yylhs.value.obj), yylhs.location);
    }
#line 1658 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 91:
#line 440 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = Py_BuildValue("(OO)", Py_None, Py_None); }
#line 1664 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 92:
#line 441 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = Py_BuildValue("(NO)", (yystack_[0].value.obj), Py_None); }
#line 1670 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 93:
#line 442 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = Py_BuildValue("(ON)", Py_None, (yystack_[0].value.obj)); }
#line 1676 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 94:
#line 443 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = Py_BuildValue("(NN)", (yystack_[2].value.obj), (yystack_[0].value.obj)); }
#line 1682 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 95:
#line 447 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = AppendList((yystack_[2].value.obj), (yystack_[0].value.obj)); }
#line 1688 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 96:
#line 448 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = StartList((yystack_[0].value.obj)); }
#line 1694 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 97:
#line 452 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = Py_BuildValue("(NN)", (yystack_[2].value.obj), (yystack_[0].value.obj)); }
#line 1700 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 98:
#line 456 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    {
      (yylhs.value.obj) = ctx->Call(kNewFunction, "(NNNNN)", (yystack_[7].value.obj), (yystack_[5].value.obj), (yystack_[3].value.obj), (yystack_[1].value.obj), (yystack_[0].value.obj));
      // Decorators is nullable and messes up the location tracking by
      // using the previous symbol as the start location for this production,
      // which is very misleading.  It is better to ignore decorators and
      // pretend the production started with DEF.  Even when decorators are
      // present the error line will be close enough to be helpful.
      //
      // TODO(dbaum): Consider making this smarter and only ignoring decorators
      // when they are empty.  Making decorators non-nullable and having two
      // productions for funcdef would be a reasonable solution.
      yylhs.location.begin = yystack_[6].location.begin;
      CHECK((yylhs.value.obj), yylhs.location);
    }
#line 1719 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 99:
#line 473 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = AppendList((yystack_[1].value.obj), (yystack_[0].value.obj)); }
#line 1725 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 100:
#line 474 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = PyList_New(0); }
#line 1731 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 101:
#line 478 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = (yystack_[1].value.obj); }
#line 1737 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 102:
#line 482 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = (yystack_[1].value.obj); }
#line 1743 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 103:
#line 483 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = PyList_New(0); }
#line 1749 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 104:
#line 495 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = AppendList((yystack_[3].value.obj), (yystack_[0].value.obj)); }
#line 1755 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 105:
#line 496 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = StartList((yystack_[0].value.obj)); }
#line 1761 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 106:
#line 500 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = Py_BuildValue("(NNN)", (yystack_[2].value.obj), (yystack_[1].value.obj), (yystack_[0].value.obj)); }
#line 1767 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 107:
#line 501 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = Py_BuildValue("(sOO)", "*", Py_None, Py_None); }
#line 1773 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 108:
#line 502 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = Py_BuildValue("(NNO)", (yystack_[1].value.obj), (yystack_[0].value.obj), Py_None); }
#line 1779 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 109:
#line 503 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = ctx->Value(kEllipsis); }
#line 1785 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 110:
#line 507 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = (yystack_[0].value.obj); }
#line 1791 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 111:
#line 508 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { Py_INCREF(Py_None); (yylhs.value.obj) = Py_None; }
#line 1797 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 112:
#line 512 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = (yystack_[0].value.obj); }
#line 1803 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 113:
#line 513 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = (yystack_[0].value.obj); }
#line 1809 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 114:
#line 514 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = ctx->Value(kEllipsis); }
#line 1815 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 115:
#line 515 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { Py_INCREF(Py_None); (yylhs.value.obj) = Py_None; }
#line 1821 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 116:
#line 519 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = PyString_FromFormat("*%s", PyString_AsString((yystack_[0].value.obj))); }
#line 1827 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 117:
#line 520 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = PyString_FromFormat("**%s", PyString_AsString((yystack_[0].value.obj))); }
#line 1833 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 118:
#line 524 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = (yystack_[0].value.obj); }
#line 1839 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 119:
#line 525 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = ctx->Value(kAnything); }
#line 1845 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 120:
#line 529 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { Py_DecRef((yystack_[0].value.obj)); }
#line 1851 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 121:
#line 533 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = (yystack_[1].value.obj); }
#line 1857 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 122:
#line 534 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = (yystack_[1].value.obj); }
#line 1863 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 123:
#line 535 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = PyList_New(0); }
#line 1869 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 131:
#line 549 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = AppendList((yystack_[1].value.obj), (yystack_[0].value.obj)); }
#line 1875 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 132:
#line 550 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = StartList((yystack_[0].value.obj)); }
#line 1881 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 133:
#line 554 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = Py_BuildValue("(NN)", (yystack_[2].value.obj), (yystack_[0].value.obj)); }
#line 1887 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 134:
#line 555 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = (yystack_[0].value.obj); }
#line 1893 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 135:
#line 556 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = (yystack_[2].value.obj); }
#line 1899 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 136:
#line 560 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = AppendList((yystack_[2].value.obj), (yystack_[0].value.obj)); }
#line 1905 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 137:
#line 561 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = StartList((yystack_[0].value.obj)); }
#line 1911 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 138:
#line 565 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = (yystack_[0].value.obj); }
#line 1917 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 139:
#line 566 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = ctx->Value(kEllipsis); }
#line 1923 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 140:
#line 570 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    {
      (yylhs.value.obj) = ctx->Call(kNewType, "(N)", (yystack_[0].value.obj));
      CHECK((yylhs.value.obj), yylhs.location);
    }
#line 1932 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 141:
#line 574 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    {
      (yylhs.value.obj) = ctx->Call(kNewType, "(NN)", (yystack_[3].value.obj), (yystack_[1].value.obj));
      CHECK((yylhs.value.obj), yylhs.location);
    }
#line 1941 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 142:
#line 578 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    {
      // This rule is needed for Callable[[...], ...]
      (yylhs.value.obj) = ctx->Call(kNewType, "(sN)", "tuple", (yystack_[1].value.obj));
      CHECK((yylhs.value.obj), yylhs.location);
    }
#line 1951 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 143:
#line 583 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    {
      (yylhs.value.obj) = ctx->Call(kNewNamedTuple, "(NN)", (yystack_[3].value.obj), (yystack_[1].value.obj));
      CHECK((yylhs.value.obj), yylhs.location);
    }
#line 1960 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 144:
#line 587 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = (yystack_[1].value.obj); }
#line 1966 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 145:
#line 588 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = ctx->Call(kNewIntersectionType, "([NN])", (yystack_[2].value.obj), (yystack_[0].value.obj)); }
#line 1972 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 146:
#line 589 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = ctx->Call(kNewUnionType, "([NN])", (yystack_[2].value.obj), (yystack_[0].value.obj)); }
#line 1978 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 147:
#line 590 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = ctx->Value(kAnything); }
#line 1984 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 148:
#line 591 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = ctx->Value(kNothing); }
#line 1990 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 149:
#line 595 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = (yystack_[2].value.obj); }
#line 1996 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 150:
#line 596 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = PyList_New(0); }
#line 2002 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 151:
#line 600 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = AppendList((yystack_[2].value.obj), (yystack_[0].value.obj)); }
#line 2008 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 152:
#line 601 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = StartList((yystack_[0].value.obj)); }
#line 2014 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 153:
#line 605 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = Py_BuildValue("(NN)", (yystack_[4].value.obj), (yystack_[2].value.obj)); }
#line 2020 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 156:
#line 614 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = (yystack_[0].value.obj); }
#line 2026 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 157:
#line 615 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = PyList_New(0); }
#line 2032 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 158:
#line 619 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = AppendList((yystack_[2].value.obj), (yystack_[0].value.obj)); }
#line 2038 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 159:
#line 620 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = StartList((yystack_[0].value.obj)); }
#line 2044 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 160:
#line 627 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = AppendList((yystack_[2].value.obj), (yystack_[0].value.obj)); }
#line 2050 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 161:
#line 628 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = Py_BuildValue("(NN)", (yystack_[2].value.obj), (yystack_[0].value.obj)); }
#line 2056 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 162:
#line 637 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    {
      Py_DECREF((yystack_[2].value.obj));
      (yylhs.value.obj) = ctx->Value(kTuple);
    }
#line 2065 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 163:
#line 642 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    {
      Py_DECREF((yystack_[2].value.obj));
      (yylhs.value.obj) = ctx->Value(kTuple);
    }
#line 2074 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 164:
#line 648 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    {
      Py_DECREF((yystack_[1].value.obj));
      (yylhs.value.obj) = ctx->Value(kTuple);
    }
#line 2083 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 165:
#line 655 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = (yystack_[0].value.obj); }
#line 2089 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 166:
#line 656 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    {
#if PY_MAJOR_VERSION >= 3
      (yystack_[2].value.obj) = PyUnicode_Concat((yystack_[2].value.obj), DOT_STRING);
      (yystack_[2].value.obj) = PyUnicode_Concat((yystack_[2].value.obj), (yystack_[0].value.obj));
      Py_DECREF((yystack_[0].value.obj));
#else
      PyString_Concat(&(yystack_[2].value.obj), DOT_STRING);
      PyString_ConcatAndDel(&(yystack_[2].value.obj), (yystack_[0].value.obj));
#endif
      (yylhs.value.obj) = (yystack_[2].value.obj);
    }
#line 2105 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 167:
#line 670 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = (yystack_[0].value.obj); }
#line 2111 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 168:
#line 671 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    {
      PyObject* slice = PySlice_New((yystack_[2].value.obj), (yystack_[0].value.obj), NULL);
      CHECK(slice, yylhs.location);
      (yylhs.value.obj) = slice;
    }
#line 2121 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 169:
#line 676 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    {
      PyObject* slice = PySlice_New((yystack_[4].value.obj), (yystack_[2].value.obj), (yystack_[0].value.obj));
      CHECK(slice, yylhs.location);
      (yylhs.value.obj) = slice;
    }
#line 2131 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 170:
#line 684 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = (yystack_[0].value.obj); }
#line 2137 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 171:
#line 685 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = NULL; }
#line 2143 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;


#line 2147 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
            default:
              break;
            }
        }
      catch (const syntax_error& yyexc)
        {
          error (yyexc);
          YYERROR;
        }
      YY_SYMBOL_PRINT ("-> $$ =", yylhs);
      yypop_ (yylen);
      yylen = 0;
      YY_STACK_PRINT ();

      // Shift the result of the reduction.
      yypush_ (YY_NULLPTR, yylhs);
    }
    goto yynewstate;

  /*--------------------------------------.
  | yyerrlab -- here on detecting error.  |
  `--------------------------------------*/
  yyerrlab:
    // If not already recovering from an error, report this error.
    if (!yyerrstatus_)
      {
        ++yynerrs_;
        error (yyla.location, yysyntax_error_ (yystack_[0].state, yyla));
      }


    yyerror_range[1].location = yyla.location;
    if (yyerrstatus_ == 3)
      {
        /* If just tried and failed to reuse lookahead token after an
           error, discard it.  */

        // Return failure if at end of input.
        if (yyla.type_get () == yyeof_)
          YYABORT;
        else if (!yyla.empty ())
          {
            yy_destroy_ ("Error: discarding", yyla);
            yyla.clear ();
          }
      }

    // Else will try to reuse lookahead token after shifting the error token.
    goto yyerrlab1;


  /*---------------------------------------------------.
  | yyerrorlab -- error raised explicitly by YYERROR.  |
  `---------------------------------------------------*/
  yyerrorlab:

    /* Pacify compilers like GCC when the user code never invokes
       YYERROR and the label yyerrorlab therefore never appears in user
       code.  */
    if (false)
      goto yyerrorlab;
    yyerror_range[1].location = yystack_[yylen - 1].location;
    /* Do not reclaim the symbols of the rule whose action triggered
       this YYERROR.  */
    yypop_ (yylen);
    yylen = 0;
    goto yyerrlab1;

  /*-------------------------------------------------------------.
  | yyerrlab1 -- common code for both syntax error and YYERROR.  |
  `-------------------------------------------------------------*/
  yyerrlab1:
    yyerrstatus_ = 3;   // Each real token shifted decrements this.
    {
      stack_symbol_type error_token;
      for (;;)
        {
          yyn = yypact_[yystack_[0].state];
          if (!yy_pact_value_is_default_ (yyn))
            {
              yyn += yyterror_;
              if (0 <= yyn && yyn <= yylast_ && yycheck_[yyn] == yyterror_)
                {
                  yyn = yytable_[yyn];
                  if (0 < yyn)
                    break;
                }
            }

          // Pop the current state because it cannot handle the error token.
          if (yystack_.size () == 1)
            YYABORT;

          yyerror_range[1].location = yystack_[0].location;
          yy_destroy_ ("Error: popping", yystack_[0]);
          yypop_ ();
          YY_STACK_PRINT ();
        }

      yyerror_range[2].location = yyla.location;
      YYLLOC_DEFAULT (error_token.location, yyerror_range, 2);

      // Shift the error token.
      error_token.state = yyn;
      yypush_ ("Shifting", error_token);
    }
    goto yynewstate;

    // Accept.
  yyacceptlab:
    yyresult = 0;
    goto yyreturn;

    // Abort.
  yyabortlab:
    yyresult = 1;
    goto yyreturn;

  yyreturn:
    if (!yyla.empty ())
      yy_destroy_ ("Cleanup: discarding lookahead", yyla);

    /* Do not reclaim the symbols of the rule whose action triggered
       this YYABORT or YYACCEPT.  */
    yypop_ (yylen);
    while (1 < yystack_.size ())
      {
        yy_destroy_ ("Cleanup: popping", yystack_[0]);
        yypop_ ();
      }

    return yyresult;
  }
    catch (...)
      {
        YYCDEBUG << "Exception caught: cleaning lookahead and stack"
                 << std::endl;
        // Do not try to display the values of the reclaimed symbols,
        // as their printer might throw an exception.
        if (!yyla.empty ())
          yy_destroy_ (YY_NULLPTR, yyla);

        while (1 < yystack_.size ())
          {
            yy_destroy_ (YY_NULLPTR, yystack_[0]);
            yypop_ ();
          }
        throw;
      }
  }

  void
  parser::error (const syntax_error& yyexc)
  {
    error (yyexc.location, yyexc.what());
  }

  // Generate an error message.
  std::string
  parser::yysyntax_error_ (state_type yystate, const symbol_type& yyla) const
  {
    // Number of reported tokens (one for the "unexpected", one per
    // "expected").
    size_t yycount = 0;
    // Its maximum.
    enum { YYERROR_VERBOSE_ARGS_MAXIMUM = 5 };
    // Arguments of yyformat.
    char const *yyarg[YYERROR_VERBOSE_ARGS_MAXIMUM];

    /* There are many possibilities here to consider:
       - If this state is a consistent state with a default action, then
         the only way this function was invoked is if the default action
         is an error action.  In that case, don't check for expected
         tokens because there are none.
       - The only way there can be no lookahead present (in yyla) is
         if this state is a consistent state with a default action.
         Thus, detecting the absence of a lookahead is sufficient to
         determine that there is no unexpected or expected token to
         report.  In that case, just report a simple "syntax error".
       - Don't assume there isn't a lookahead just because this state is
         a consistent state with a default action.  There might have
         been a previous inconsistent state, consistent state with a
         non-default action, or user semantic action that manipulated
         yyla.  (However, yyla is currently not documented for users.)
       - Of course, the expected token list depends on states to have
         correct lookahead information, and it depends on the parser not
         to perform extra reductions after fetching a lookahead from the
         scanner and before detecting a syntax error.  Thus, state
         merging (from LALR or IELR) and default reductions corrupt the
         expected token list.  However, the list is correct for
         canonical LR with one exception: it will still contain any
         token that will not be accepted due to an error action in a
         later state.
    */
    if (!yyla.empty ())
      {
        int yytoken = yyla.type_get ();
        yyarg[yycount++] = yytname_[yytoken];
        int yyn = yypact_[yystate];
        if (!yy_pact_value_is_default_ (yyn))
          {
            /* Start YYX at -YYN if negative to avoid negative indexes in
               YYCHECK.  In other words, skip the first -YYN actions for
               this state because they are default actions.  */
            int yyxbegin = yyn < 0 ? -yyn : 0;
            // Stay within bounds of both yycheck and yytname.
            int yychecklim = yylast_ - yyn + 1;
            int yyxend = yychecklim < yyntokens_ ? yychecklim : yyntokens_;
            for (int yyx = yyxbegin; yyx < yyxend; ++yyx)
              if (yycheck_[yyx + yyn] == yyx && yyx != yyterror_
                  && !yy_table_value_is_error_ (yytable_[yyx + yyn]))
                {
                  if (yycount == YYERROR_VERBOSE_ARGS_MAXIMUM)
                    {
                      yycount = 1;
                      break;
                    }
                  else
                    yyarg[yycount++] = yytname_[yyx];
                }
          }
      }

    char const* yyformat = YY_NULLPTR;
    switch (yycount)
      {
#define YYCASE_(N, S)                         \
        case N:                               \
          yyformat = S;                       \
        break
        YYCASE_(0, YY_("syntax error"));
        YYCASE_(1, YY_("syntax error, unexpected %s"));
        YYCASE_(2, YY_("syntax error, unexpected %s, expecting %s"));
        YYCASE_(3, YY_("syntax error, unexpected %s, expecting %s or %s"));
        YYCASE_(4, YY_("syntax error, unexpected %s, expecting %s or %s or %s"));
        YYCASE_(5, YY_("syntax error, unexpected %s, expecting %s or %s or %s or %s"));
#undef YYCASE_
      }

    std::string yyres;
    // Argument number.
    size_t yyi = 0;
    for (char const* yyp = yyformat; *yyp; ++yyp)
      if (yyp[0] == '%' && yyp[1] == 's' && yyi < yycount)
        {
          yyres += yytnamerr_ (yyarg[yyi++]);
          ++yyp;
        }
      else
        yyres += *yyp;
    return yyres;
  }


  const short int parser::yypact_ninf_ = -219;

  const short int parser::yytable_ninf_ = -171;

  const short int
  parser::yypact_[] =
  {
     -16,  -219,    41,    86,   326,    92,  -219,  -219,   116,   111,
      12,   137,    15,  -219,  -219,   196,   -14,  -219,  -219,  -219,
    -219,  -219,    16,  -219,   182,    13,  -219,   130,  -219,    12,
     224,   267,   141,  -219,    -2,    39,   152,   144,  -219,    12,
     192,   212,   171,   244,   137,  -219,  -219,   181,   182,   182,
    -219,   132,   241,  -219,   255,   232,  -219,  -219,   182,   110,
    -219,    45,   266,    99,    12,    12,  -219,  -219,  -219,  -219,
     300,  -219,  -219,   307,    74,   137,   309,     9,    17,  -219,
       9,   224,   295,   308,  -219,   311,    36,   340,   195,   258,
     288,   313,   182,   182,   347,   330,  -219,  -219,   154,   350,
     182,   101,   318,  -219,   319,  -219,   261,  -219,   258,   325,
    -219,   345,  -219,   327,   320,   328,  -219,  -219,   354,  -219,
    -219,  -219,   346,  -219,  -219,    85,  -219,  -219,   329,  -219,
    -219,  -219,  -219,   238,    27,  -219,   331,  -219,  -219,   182,
     351,  -219,  -219,   325,  -219,   222,  -219,   258,   332,   283,
     176,   182,   334,   182,  -219,   184,   317,   293,   360,   335,
     363,   289,    85,   240,   257,  -219,   337,  -219,     7,   338,
     336,  -219,   337,   339,   258,  -219,   154,  -219,   194,   341,
    -219,  -219,   258,   258,  -219,   258,  -219,  -219,  -219,   167,
    -219,   325,    61,  -219,   342,   103,  -219,  -219,    19,  -219,
    -219,  -219,   182,   343,  -219,   371,   357,    -9,  -219,  -219,
     225,   344,  -219,   348,   352,  -219,   353,  -219,    62,   355,
     228,  -219,  -219,  -219,  -219,   360,   312,  -219,  -219,   258,
     299,  -219,  -219,   182,   349,    27,   378,  -219,   356,  -219,
    -219,   182,   381,   194,   358,  -219,   305,  -219,  -219,   196,
     361,  -219,  -219,  -219,  -219,  -219,   383,  -219,  -219,  -219,
     258,   301,  -219,  -219,  -219,   359,   362,   364,   258,   348,
    -219,   352,  -219,   129,   365,   366,   370,   367,   220,   324,
     325,   182,  -219,  -219,   373,   374,  -219,  -219,   368,   182,
     376,   165,  -219,   379,   298,  -219,  -219,   147,  -219,  -219,
     270,   182,   108,  -219,  -219,  -219,  -219,   223,   380,  -219,
     375,   272,   278,  -219,   258,   377,  -219,  -219,  -219,  -219,
    -219,  -219
  };

  const unsigned char
  parser::yydefact_[] =
  {
      12,    12,     0,     0,   100,     0,     1,     2,     0,     0,
       0,     0,     0,     9,    11,    36,     0,     5,     7,     8,
      10,     6,     0,     3,     0,     0,    16,    19,   165,     0,
      43,     0,    70,    74,    75,     0,     0,    77,    45,     0,
       0,     0,     0,     0,     0,    99,   148,     0,     0,   157,
     147,    14,   140,    62,     0,    66,    63,    64,     0,    89,
      65,     0,     0,     0,     0,     0,    60,    61,    58,    59,
     171,    56,    57,     0,     0,     0,     0,     0,     0,    78,
       0,    44,     0,     0,    12,     0,    14,     0,     0,   159,
       0,   156,     0,     0,     0,     0,    68,    13,     0,     0,
       0,     0,   155,   164,   165,    18,     0,    21,    22,    14,
      52,    51,    50,   167,     0,     0,   166,    46,     0,    47,
      73,    76,    84,    85,    86,     0,    87,    72,    79,    83,
      71,    12,    12,   100,   103,   101,     0,   144,   142,     0,
     146,   145,   120,    14,   139,     0,   137,   138,    91,    14,
       0,   154,     0,     0,    17,     0,     0,     0,   171,     0,
       0,     0,     0,   100,   100,    37,   111,   109,   107,     0,
     155,   105,   111,     0,   158,    69,     0,   141,     0,     0,
      67,   163,   161,   160,   162,    23,    20,   172,   173,    34,
      15,    14,     0,   170,   168,     0,    88,    80,     0,    82,
      38,    35,     0,   115,   116,     0,   119,    14,   102,   108,
       0,     0,   136,   165,    93,    96,    92,    90,    34,     0,
     100,    27,    24,    48,    49,   171,     0,    53,    81,   110,
       0,   106,   117,     0,   130,     0,     0,   150,   155,   152,
     143,     0,     0,     0,     0,    25,     0,    33,    32,    40,
       0,    29,    30,    31,   169,    54,     0,   112,   113,   114,
     118,     0,    98,   123,   104,     0,   154,     0,    97,     0,
      95,    94,    26,     0,     0,     0,     0,     0,     0,     0,
     124,     0,   151,   149,     0,     0,    34,    55,     0,     0,
       0,     0,   132,     0,     0,   126,   125,   155,    34,    34,
     100,     0,   134,   129,   122,   131,   128,     0,     0,   154,
       0,   100,   100,    41,   133,     0,   121,   127,   153,    42,
      39,   135
  };

  const short int
  parser::yypgoto_[] =
  {
    -219,  -219,   389,   -76,   -82,  -218,  -219,  -219,  -219,   236,
    -219,   175,   -12,  -219,  -219,  -219,  -219,  -215,   157,   160,
     126,   219,   256,  -213,  -219,  -219,   369,   402,   372,   290,
    -126,  -211,  -219,  -219,   173,   177,  -209,  -219,  -219,  -219,
    -219,   183,   245,  -219,  -219,  -219,  -105,  -219,  -219,   127,
     -83,  -219,   246,   -24,  -219,  -219,   158,  -167,  -219,   242,
    -219,  -219,   106,  -219,  -152,  -155
  };

  const short int
  parser::yydefgoto_[] =
  {
      -1,     2,     3,     4,    96,    13,    27,    62,   106,   107,
     190,   219,   220,    14,    15,   248,   249,    16,    40,    41,
      30,   119,    74,    17,    18,    32,    33,    79,   127,   128,
     129,    19,    20,   179,   214,   215,    21,    22,    45,   169,
     170,   171,   203,   231,   172,   234,    97,   262,   263,   291,
     292,   145,   146,    59,   211,   238,   239,   152,    90,    91,
     102,    60,    52,   114,   115,   221
  };

  const short int
  parser::yytable_[] =
  {
      51,   191,   247,   208,   135,   250,   194,   251,   133,   252,
     204,   253,   122,     1,    76,    28,    28,    53,    28,    42,
      28,    94,   122,    43,    88,    89,  -154,   156,   123,   124,
     166,    46,    47,    54,   101,    55,   199,   108,   123,   124,
      73,     6,    28,   125,    56,    57,    29,    58,   104,   167,
     205,    49,   126,    77,   228,   163,   164,    35,    50,    78,
      44,   175,   126,    46,    47,   223,    94,   180,   140,   141,
     168,   267,   199,   254,   147,   187,   149,   117,    73,    48,
     105,    78,   247,    49,   188,   250,     7,   251,   122,   252,
      50,   253,    23,   247,   247,   118,   250,   250,   251,   251,
     252,   252,   253,   253,   123,   124,   280,   226,   118,   222,
      64,    65,    92,    93,    26,   174,    31,    34,    37,    92,
      93,    92,    93,   293,   295,   235,   182,   183,   126,   185,
     310,   108,    28,    53,   110,    31,   137,   150,   227,   308,
      28,    37,   315,    92,    93,    31,   103,    46,    47,    24,
      86,    55,   147,    25,    89,    63,   279,    28,    92,    93,
      56,    57,    94,    58,    61,    81,    80,    49,   288,    95,
      31,    31,    46,    47,    50,   296,   144,    75,   229,    28,
     187,    34,   289,   309,    37,    28,    73,   104,    48,   188,
     111,   112,    49,   304,    46,    47,   218,   213,    84,    50,
      46,    47,    46,    47,    38,    39,    92,    93,   305,   260,
      48,   181,    46,    47,    49,    87,    48,   268,    48,   174,
      49,    50,    49,   288,   305,    82,   288,    50,    48,    50,
     137,   246,    49,   187,     9,    64,    65,   289,    10,    50,
     289,     8,   188,     8,     9,    83,     9,    85,    10,   290,
      10,   316,    11,    12,    11,    12,   -28,   297,   176,   236,
       8,   177,   100,     9,   237,   302,   165,    10,   200,    92,
      93,    11,    12,   246,   300,   246,     9,   314,     9,    98,
      10,   246,    10,    73,     9,   201,   311,   312,    10,    99,
      66,    67,    68,    69,    92,    93,   154,   155,   313,   109,
     319,   288,   257,   258,   113,    70,   320,    71,    72,    73,
     116,   187,   121,    94,   187,   289,    66,    67,    68,    69,
     188,   259,   131,   188,   197,   198,    -4,   138,   278,     8,
     187,    94,     9,    71,    72,   132,    10,   187,    24,   188,
      11,    12,   273,   136,   189,   134,   188,   255,   256,   139,
     142,   294,   143,   148,   151,    94,   153,    65,   159,   157,
    -170,   158,   160,    93,   193,   162,   196,   173,   178,   184,
     202,   195,   207,   206,   232,   225,   217,   210,   233,   240,
     230,   265,   261,   245,   269,   241,   272,   277,   242,   243,
       5,   186,   266,   244,   276,   281,   236,   286,   284,   285,
     298,   299,   287,   283,   303,   301,   274,   306,   317,   275,
     318,   224,   321,   192,    36,   161,   271,   209,   264,   270,
     216,   307,   212,     0,   282,     0,     0,     0,     0,     0,
       0,     0,     0,     0,     0,     0,     0,     0,     0,     0,
       0,     0,     0,     0,   120,     0,     0,     0,     0,     0,
       0,     0,   130
  };

  const short int
  parser::yycheck_[] =
  {
      24,   156,   220,   170,    86,   220,   158,   220,    84,   220,
       3,   220,     3,    29,    16,     3,     3,     4,     3,    33,
       3,    30,     3,     7,    48,    49,    35,   109,    19,    20,
       3,    18,    19,    20,    58,    22,   162,    61,    19,    20,
      42,     0,     3,    34,    31,    32,    34,    34,     3,    22,
      43,    38,    43,    14,    35,   131,   132,    42,    45,    42,
      44,   143,    43,    18,    19,     4,    30,   149,    92,    93,
      43,   238,   198,   225,    98,    13,   100,     3,    42,    34,
      35,    42,   300,    38,    22,   300,     0,   300,     3,   300,
      45,   300,     0,   311,   312,    34,   311,   312,   311,   312,
     311,   312,   311,   312,    19,    20,   261,     4,    34,   191,
      11,    12,    11,    12,     3,   139,    10,    11,    12,    11,
      12,    11,    12,   278,   279,   207,   150,   151,    43,   153,
     297,   155,     3,     4,    35,    29,    35,    36,    35,   294,
       3,    35,    34,    11,    12,    39,    36,    18,    19,    33,
      44,    22,   176,    37,   178,    29,   261,     3,    11,    12,
      31,    32,    30,    34,    34,    39,    14,    38,     3,    37,
      64,    65,    18,    19,    45,   280,    22,    36,   202,     3,
      13,    75,    17,    36,    78,     3,    42,     3,    34,    22,
      64,    65,    38,    28,    18,    19,    29,     3,    27,    45,
      18,    19,    18,    19,     8,     9,    11,    12,   291,   233,
      34,    35,    18,    19,    38,    34,    34,   241,    34,   243,
      38,    45,    38,     3,   307,    33,     3,    45,    34,    45,
      35,     3,    38,    13,     6,    11,    12,    17,    10,    45,
      17,     3,    22,     3,     6,    33,     6,     3,    10,    29,
      10,    28,    14,    15,    14,    15,    28,   281,    36,    34,
       3,    39,    30,     6,    39,   289,    28,    10,    28,    11,
      12,    14,    15,     3,   286,     3,     6,   301,     6,    38,
      10,     3,    10,    42,     6,    28,   298,   299,    10,    34,
      23,    24,    25,    26,    11,    12,    35,    36,    28,    33,
      28,     3,     3,     4,     4,    38,    28,    40,    41,    42,
       3,    13,     3,    30,    13,    17,    23,    24,    25,    26,
      22,    22,    27,    22,    35,    36,     0,    39,    27,     3,
      13,    30,     6,    40,    41,    27,    10,    13,    33,    22,
      14,    15,    37,     3,    27,    34,    22,    35,    36,    36,
       3,    27,    22,     3,    36,    30,    37,    12,     4,    39,
      33,    33,    16,    12,     4,    36,     3,    36,    36,    35,
      33,    36,    36,    35,     3,    33,    35,    38,    21,    35,
      37,     3,    33,    28,     3,    37,    28,     4,    36,    36,
       1,   155,    36,   218,    33,    36,    34,    27,    33,    33,
      27,    27,    35,    39,    28,    37,   249,    28,    28,   249,
      35,   192,    35,   157,    12,   125,   243,   172,   235,   242,
     178,   294,   176,    -1,   266,    -1,    -1,    -1,    -1,    -1,
      -1,    -1,    -1,    -1,    -1,    -1,    -1,    -1,    -1,    -1,
      -1,    -1,    -1,    -1,    75,    -1,    -1,    -1,    -1,    -1,
      -1,    -1,    80
  };

  const unsigned char
  parser::yystos_[] =
  {
       0,    29,    47,    48,    49,    48,     0,     0,     3,     6,
      10,    14,    15,    51,    59,    60,    63,    69,    70,    77,
      78,    82,    83,     0,    33,    37,     3,    52,     3,    34,
      66,   108,    71,    72,   108,    42,    73,   108,     8,     9,
      64,    65,    33,     7,    44,    84,    18,    19,    34,    38,
      45,    99,   108,     4,    20,    22,    31,    32,    34,    99,
     107,    34,    53,    66,    11,    12,    23,    24,    25,    26,
      38,    40,    41,    42,    68,    36,    16,    14,    42,    73,
      14,    66,    33,    33,    27,     3,   108,    34,    99,    99,
     104,   105,    11,    12,    30,    37,    50,    92,    38,    34,
      30,    99,   106,    36,     3,    35,    54,    55,    99,    33,
      35,    66,    66,     4,   109,   110,     3,     3,    34,    67,
      72,     3,     3,    19,    20,    34,    43,    74,    75,    76,
      74,    27,    27,    49,    34,    50,     3,    35,    39,    36,
      99,    99,     3,    22,    22,    97,    98,    99,     3,    99,
      36,    36,   103,    37,    35,    36,    50,    39,    33,     4,
      16,    75,    36,    49,    49,    28,     3,    22,    43,    85,
      86,    87,    90,    36,    99,    50,    36,    39,    36,    79,
      50,    35,    99,    99,    35,    99,    55,    13,    22,    27,
      56,   111,    68,     4,   110,    36,     3,    35,    36,    76,
      28,    28,    33,    88,     3,    43,    35,    36,   103,    88,
      38,   100,    98,     3,    80,    81,   105,    35,    29,    57,
      58,   111,    50,     4,    67,    33,     4,    35,    35,    99,
      37,    89,     3,    21,    91,    50,    34,    39,   101,   102,
      35,    37,    36,    36,    57,    28,     3,    51,    61,    62,
      63,    69,    77,    82,   110,    35,    36,     3,     4,    22,
      99,    33,    93,    94,    87,     3,    36,   103,    99,     3,
      81,    80,    28,    37,    64,    65,    33,     4,    27,    92,
     111,    36,   102,    39,    33,    33,    27,    35,     3,    17,
      29,    95,    96,   111,    27,   111,    92,    99,    27,    27,
      58,    37,    99,    28,    28,    96,    28,    95,   111,    36,
     103,    58,    58,    28,    99,    34,    28,    28,    35,    28,
      28,    35
  };

  const unsigned char
  parser::yyr1_[] =
  {
       0,    46,    47,    47,    48,    49,    49,    49,    49,    49,
      49,    49,    49,    50,    50,    51,    52,    53,    53,    53,
      54,    54,    55,    55,    56,    56,    56,    57,    57,    58,
      58,    58,    58,    58,    58,    59,    59,    60,    60,    61,
      61,    62,    62,    63,    64,    65,    66,    66,    66,    66,
      66,    66,    66,    67,    67,    67,    68,    68,    68,    68,
      68,    68,    69,    69,    69,    69,    69,    69,    69,    69,
      70,    70,    70,    71,    71,    72,    72,    73,    73,    74,
      74,    74,    75,    75,    76,    76,    76,    76,    76,    77,
      78,    79,    79,    79,    79,    80,    80,    81,    82,    83,
      83,    84,    85,    85,    86,    86,    87,    87,    87,    87,
      88,    88,    89,    89,    89,    89,    90,    90,    91,    91,
      92,    93,    93,    93,    94,    94,    94,    94,    94,    94,
      94,    95,    95,    96,    96,    96,    97,    97,    98,    98,
      99,    99,    99,    99,    99,    99,    99,    99,    99,   100,
     100,   101,   101,   102,   103,   103,   104,   104,   105,   105,
     106,   106,   107,   107,   107,   108,   108,   109,   109,   109,
     110,   110,   111,   111
  };

  const unsigned char
  parser::yyr2_[] =
  {
       0,     2,     2,     3,     1,     2,     2,     2,     2,     2,
       2,     2,     0,     1,     0,     6,     1,     3,     2,     0,
       3,     1,     1,     3,     2,     3,     4,     1,     1,     2,
       2,     2,     2,     2,     0,     6,     1,     5,     6,     6,
       1,     5,     6,     2,     2,     1,     3,     3,     6,     6,
       3,     3,     3,     4,     5,     7,     1,     1,     1,     1,
       1,     1,     3,     3,     3,     3,     3,     6,     4,     6,
       2,     4,     4,     3,     1,     1,     3,     1,     2,     1,
       3,     4,     3,     1,     1,     1,     1,     1,     3,     3,
       7,     0,     2,     2,     4,     3,     1,     3,     8,     2,
       0,     3,     2,     0,     4,     1,     3,     1,     2,     1,
       2,     0,     2,     2,     2,     0,     2,     3,     2,     0,
       2,     5,     4,     1,     2,     3,     3,     5,     4,     4,
       0,     2,     1,     3,     2,     4,     3,     1,     1,     1,
       1,     4,     3,     6,     3,     3,     3,     1,     1,     4,
       2,     3,     1,     6,     1,     0,     1,     0,     3,     1,
       3,     3,     4,     4,     2,     1,     3,     1,     3,     5,
       1,     0,     1,     1
  };



  // YYTNAME[SYMBOL-NUM] -- String name of the symbol SYMBOL-NUM.
  // First, the terminals, then, starting at \a yyntokens_, nonterminals.
  const char*
  const parser::yytname_[] =
  {
  "\"end of file\"", "error", "$undefined", "NAME", "NUMBER", "LEXERROR",
  "CLASS", "DEF", "ELSE", "ELIF", "IF", "OR", "AND", "PASS", "IMPORT",
  "FROM", "AS", "RAISE", "NOTHING", "NAMEDTUPLE", "TYPEVAR", "ARROW",
  "ELLIPSIS", "EQ", "NE", "LE", "GE", "INDENT", "DEDENT", "TRIPLEQUOTED",
  "TYPECOMMENT", "BYTESTRING", "UNICODESTRING", "':'", "'('", "')'", "','",
  "'='", "'['", "']'", "'<'", "'>'", "'.'", "'*'", "'@'", "'?'", "$accept",
  "start", "unit", "alldefs", "maybe_type_ignore", "classdef",
  "class_name", "parents", "parent_list", "parent", "maybe_class_funcs",
  "class_funcs", "funcdefs", "if_stmt", "if_and_elifs", "class_if_stmt",
  "class_if_and_elifs", "if_cond", "elif_cond", "else_cond", "condition",
  "version_tuple", "condition_op", "constantdef", "importdef",
  "import_items", "import_item", "import_name", "from_list", "from_items",
  "from_item", "alias_or_constant", "typevardef", "typevar_args",
  "typevar_kwargs", "typevar_kwarg", "funcdef", "decorators", "decorator",
  "params", "param_list", "param", "param_type", "param_default",
  "param_star_name", "return", "typeignore", "maybe_body", "empty_body",
  "body", "body_stmt", "type_parameters", "type_parameter", "type",
  "named_tuple_fields", "named_tuple_field_list", "named_tuple_field",
  "maybe_comma", "maybe_type_list", "type_list", "type_tuple_elements",
  "type_tuple_literal", "dotted_name", "getitem_key", "maybe_number",
  "pass_or_ellipsis", YY_NULLPTR
  };

#if YYDEBUG
  const unsigned short int
  parser::yyrline_[] =
  {
       0,   132,   132,   133,   137,   141,   142,   143,   144,   150,
     151,   152,   157,   161,   162,   168,   175,   186,   187,   188,
     192,   193,   197,   198,   202,   203,   204,   208,   209,   213,
     214,   219,   220,   225,   226,   231,   234,   239,   243,   262,
     265,   270,   274,   286,   290,   294,   298,   301,   304,   307,
     310,   311,   312,   317,   318,   319,   325,   326,   327,   328,
     329,   330,   334,   338,   342,   346,   350,   354,   358,   362,
     369,   373,   377,   386,   387,   390,   391,   396,   397,   404,
     405,   406,   410,   411,   415,   416,   419,   422,   425,   429,
     433,   440,   441,   442,   443,   447,   448,   452,   456,   473,
     474,   478,   482,   483,   495,   496,   500,   501,   502,   503,
     507,   508,   512,   513,   514,   515,   519,   520,   524,   525,
     529,   533,   534,   535,   539,   540,   541,   542,   543,   544,
     545,   549,   550,   554,   555,   556,   560,   561,   565,   566,
     570,   574,   578,   583,   587,   588,   589,   590,   591,   595,
     596,   600,   601,   605,   609,   610,   614,   615,   619,   620,
     627,   628,   637,   642,   648,   655,   656,   670,   671,   676,
     684,   685,   689,   690
  };

  // Print the state stack on the debug stream.
  void
  parser::yystack_print_ ()
  {
    *yycdebug_ << "Stack now";
    for (stack_type::const_iterator
           i = yystack_.begin (),
           i_end = yystack_.end ();
         i != i_end; ++i)
      *yycdebug_ << ' ' << i->state;
    *yycdebug_ << std::endl;
  }

  // Report on the debug stream that the rule \a yyrule is going to be reduced.
  void
  parser::yy_reduce_print_ (int yyrule)
  {
    unsigned int yylno = yyrline_[yyrule];
    int yynrhs = yyr2_[yyrule];
    // Print the symbols being reduced, and their result.
    *yycdebug_ << "Reducing stack by rule " << yyrule - 1
               << " (line " << yylno << "):" << std::endl;
    // The symbols being reduced.
    for (int yyi = 0; yyi < yynrhs; yyi++)
      YY_SYMBOL_PRINT ("   $" << yyi + 1 << " =",
                       yystack_[(yynrhs) - (yyi + 1)]);
  }
#endif // YYDEBUG

  // Symbol number corresponding to token number t.
  inline
  parser::token_number_type
  parser::yytranslate_ (int t)
  {
    static
    const token_number_type
    translate_table[] =
    {
     0,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
      34,    35,    43,     2,    36,     2,    42,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,    33,     2,
      40,    37,    41,    45,    44,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,    38,     2,    39,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     1,     2,     3,     4,
       5,     6,     7,     8,     9,    10,    11,    12,    13,    14,
      15,    16,    17,    18,    19,    20,    21,    22,    23,    24,
      25,    26,    27,    28,    29,    30,    31,    32
    };
    const unsigned int user_token_number_max_ = 287;
    const token_number_type undef_token_ = 2;

    if (static_cast<int>(t) <= yyeof_)
      return yyeof_;
    else if (static_cast<unsigned int> (t) <= user_token_number_max_)
      return translate_table[t];
    else
      return undef_token_;
  }

#line 17 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:1167
} // pytype
#line 2827 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:1167
#line 693 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:1168


void pytype::parser::error(const location& loc, const std::string& msg) {
  ctx->SetErrorLocation(loc);
  pytype::Lexer* lexer = pytypeget_extra(scanner);
  if (lexer->error_message_) {
    PyErr_SetObject(ctx->Value(pytype::kParseError), lexer->error_message_);
  } else {
    PyErr_SetString(ctx->Value(pytype::kParseError), msg.c_str());
  }
}

namespace {

PyObject* StartList(PyObject* item) {
  return Py_BuildValue("[N]", item);
}

PyObject* AppendList(PyObject* list, PyObject* item) {
  PyList_Append(list, item);
  Py_DECREF(item);
  return list;
}

PyObject* ExtendList(PyObject* dst, PyObject* src) {
  // Add items from src to dst (both of which must be lists) and return src.
  // Borrows the reference to src.
  Py_ssize_t count = PyList_Size(src);
  for (Py_ssize_t i=0; i < count; ++i) {
    PyList_Append(dst, PyList_GetItem(src, i));
  }
  Py_DECREF(src);
  return dst;
}

}  // end namespace
